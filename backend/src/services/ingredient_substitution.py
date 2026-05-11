"""
ingredient_substitution.py
--------------------------
Core ML service for the "Smart Ingredient Switch" feature.

Pipeline
--------
1. Feature Engineering
   - Semantic text: sentence-transformers/all-MiniLM-L6-v2 encodes
     "{product_name} | {sub_category} | {brands}" → 384-d unit vector.
   - Nutritional features: [proteins, fat, carbs, energy] z-scored then
     scaled by NUTRITION_WEIGHT (default 0.3) before concatenation.
   - Final vector: 388-d (384 semantic + 4 nutritional).

2. FAISS IVFFlat index (nlist=256) over all 33k ingredients.
   - Built by `build_index(db)`, persisted to the DB via IngredientEmbedding
     and SubstitutionMeta tables.
   - Loaded at startup by `load_index(db)`.

3. Stage-1 Candidate Generation
   - K=50 ANN neighbours retrieved.
   - Filtered by matching `functional_role` (derived from sub_category).

4. Stage-2 Multi-Objective Ranking
   - Budget:    score = 1 - min-max(retail_price)
   - Nutrition: score = 0.6 * nutri_grade + 0.4 * min-max(proteins)
   - Balanced:  score = 0.5 * budget_score + 0.5 * nutrition_score
   - Top-1 for each objective returned (with diversity enforcement).

Usage
-----
    engine = IngredientSubstitutionEngine()
    engine.load_index(db)   # or build_index(db) for first-time setup
    result = engine.get_substitutes("0001234567890", db)
"""
from __future__ import annotations

import logging
import pickle
import re
from dataclasses import dataclass
from typing import Optional

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Hyper-parameters
# ---------------------------------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
NUTRITION_WEIGHT: float = 0.3   # weight applied to z-scored nutritional dims
ANN_K: int = 50                 # neighbours to fetch before role-filtering
NLIST: int = 256                # IVF Voronoi cells (covers 33k comfortably)
BALANCED_LAMBDA: float = 0.5    # λ for budget vs nutrition in balanced score
SCALER_META_KEY = "scaler"      # key used in SubstitutionMeta table

NUTRI_GRADE_MAP: dict[str | None, float] = {
    "a": 1.0, "b": 0.8, "c": 0.6, "d": 0.4, "e": 0.2, None: 0.3
}

# ---------------------------------------------------------------------------
# Functional role mapping (keyed on sub_category from ingredient_price)
# ---------------------------------------------------------------------------
_ROLE_PATTERNS: list[tuple[str, list[str]]] = [
    ("protein",       ["meat", "poultry", "beef", "pork", "lamb", "chicken",
                       "turkey", "fish", "seafood", "salmon", "tuna", "prawn",
                       "shrimp", "shellfish"]),
    ("dairy_protein", ["dairy", "milk", "cheese", "yogurt", "yoghurt",
                       "butter", "cream", "egg"]),
    ("plant_protein", ["legume", "bean", "lentil", "tofu", "tempeh",
                       "chickpea", "pea protein", "soy"]),
    ("carb",          ["grain", "pasta", "noodle", "bread", "rice", "flour",
                       "cereal", "oat", "wheat", "corn", "potato", "starch"]),
    ("vegetable",     ["vegetable", "salad", "broccoli", "spinach", "carrot",
                       "onion", "tomato", "lettuce", "cabbage", "zucchini",
                       "capsicum", "mushroom"]),
    ("fruit",         ["fruit", "apple", "banana", "berry", "orange",
                       "mango", "grape", "citrus", "stone fruit"]),
    ("fat",           ["oil", "fat", "olive", "canola", "coconut oil",
                       "spread", "margarine", "lard", "ghee"]),
    ("flavour",       ["sauce", "condiment", "spice", "herb", "seasoning",
                       "vinegar", "mustard", "ketchup", "relish", "paste",
                       "dressing", "marinade"]),
    ("beverage",      ["beverage", "drink", "juice", "water", "coffee",
                       "tea", "soft drink", "soda", "wine", "beer"]),
]


def _infer_role(sub_category: Optional[str]) -> str:
    """Map a sub_category string to a functional role label."""
    if not sub_category or not isinstance(sub_category, str):
        return "other"
    text = sub_category.lower()
    for role, keywords in _ROLE_PATTERNS:
        if any(kw in text for kw in keywords):
            return role
    return "other"


# ---------------------------------------------------------------------------
# Data classes for structured results
# ---------------------------------------------------------------------------
@dataclass
class SubstituteSlot:
    ingredient_code: str
    product_name: str
    brands: Optional[str]
    sub_category: Optional[str]
    retail_price: Optional[float]
    nutrition_grade: Optional[str]
    proteins_100g: Optional[float]
    fat_100g: Optional[float]
    carbohydrates_100g: Optional[float]
    energy_100g: Optional[float]
    similarity_score: float
    objective_score: float


@dataclass
class SubstituteResult:
    query_code: str
    query_name: str
    budget: Optional[SubstituteSlot] = None
    nutrition: Optional[SubstituteSlot] = None
    balanced: Optional[SubstituteSlot] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Main engine
# ---------------------------------------------------------------------------
class IngredientSubstitutionEngine:
    """
    Singleton-friendly substitution engine.

    Typical lifecycle:
        engine = IngredientSubstitutionEngine()
        engine.load_index(db)        # fast path – reads pre-seeded DB rows
        result = engine.get_substitutes(code, db)

    First-time (or rebuild):
        engine = IngredientSubstitutionEngine()
        engine.build_index(db)       # seeds IngredientEmbedding + SubstitutionMeta
    """

    def __init__(self) -> None:
        self._model: Optional[SentenceTransformer] = None
        self._index: Optional[faiss.Index] = None
        self._df: Optional[pd.DataFrame] = None
        self._scaler: Optional[StandardScaler] = None
        self._ready: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_index(self, db: Session, *, df: pd.DataFrame | None = None) -> None:
        """
        Pull all data from the database, build the hybrid embedding matrix,
        fit a FAISS index, then persist both the embeddings and the scaler
        to the DB (IngredientEmbedding and SubstitutionMeta tables).

        Parameters
        ----------
        db : Session
            SQLAlchemy session used to load ingredient data and write results.
            Ignored for the initial data-load when ``df`` is supplied directly.
        df : pd.DataFrame, optional
            Pre-built DataFrame with the expected schema.  When supplied the
            DB query is skipped entirely (test injection path).

        Expected runtime on CPU with 33k ingredients: ~3–5 minutes
        (dominated by the SentenceTransformer encode pass).
        """
        # Lazy import to avoid transitive geoalchemy2 dependency at module load
        from src.models import IngredientEmbedding, SubstitutionMeta  # noqa: PLC0415

        logger.info("Building substitution index from database…")
        if df is None:
            df = self._load_dataframe(db)
        logger.info("Loaded %d ingredients.", len(df))

        df = self._impute_nutrition(df)
        embeddings = self._build_embeddings(df)     # also sets self._scaler
        index = self._build_faiss_index(embeddings)

        # ── Persist embeddings ────────────────────────────────────────────
        logger.info("Seeding IngredientEmbedding table (%d rows)…", len(df))

        macro_cols = ["proteins_100g", "fat_100g", "carbohydrates_100g", "energy_100g"]

        try:
            db.query(IngredientEmbedding).delete()

            embedding_objects = [
                IngredientEmbedding(
                    ingredient_code=code,
                    # Store as raw float32 bytes; recovered with np.frombuffer
                    embedding=df.at[code, "_embedding"].astype("float32").tobytes(),
                    functional_role=df.at[code, "functional_role"],
                    proteins_100g=_nullable_float(df.at[code, "proteins_100g"]),
                    fat_100g=_nullable_float(df.at[code, "fat_100g"]),
                    carbohydrates_100g=_nullable_float(df.at[code, "carbohydrates_100g"]),
                    energy_100g=_nullable_float(df.at[code, "energy_100g"]),
                )
                for code in df.index
            ]
            db.bulk_save_objects(embedding_objects)

            # ── Persist scaler ────────────────────────────────────────────
            logger.info("Seeding SubstitutionMeta (scaler)…")
            db.query(SubstitutionMeta).delete()
            db.add(SubstitutionMeta(
                key=SCALER_META_KEY,
                value=pickle.dumps(self._scaler, protocol=pickle.HIGHEST_PROTOCOL),
            ))

            db.commit()
            logger.info("Substitution index seeded successfully.")

        except Exception:
            db.rollback()
            logger.exception("Failed to seed substitution index; transaction rolled back.")
            raise

        self._index = index
        self._df = df
        self._ready = True
        logger.info(
            "Index ready. vectors=%d, dim=%d",
            index.ntotal, embeddings.shape[1],
        )

    def load_index(self, db: Session) -> bool:
        """
        Reconstruct the FAISS index and in-memory DataFrame from the DB.
        Returns True on success, False when the tables are empty (run
        build_index first).

        Parameters
        ----------
        db : Session
            SQLAlchemy session used to query IngredientEmbedding and
            SubstitutionMeta.
        """
        from src.models import IngredientEmbedding, SubstitutionMeta  # noqa: PLC0415

        # ── Load scaler ───────────────────────────────────────────────────
        meta_row = db.query(SubstitutionMeta).filter_by(key=SCALER_META_KEY).first()
        if meta_row is None:
            logger.warning(
                "SubstitutionMeta has no '%s' row. "
                "Run build_index(db) or the build script first.",
                SCALER_META_KEY,
            )
            return False

        self._scaler = pickle.loads(meta_row.value)

        # ── Load embeddings ───────────────────────────────────────────────
        rows = db.query(IngredientEmbedding).all()
        if not rows:
            logger.warning(
                "IngredientEmbedding table is empty. "
                "Run build_index(db) or the build script first."
            )
            return False

        logger.info("Loading %d embeddings from DB…", len(rows))

        codes, vecs, roles = [], [], []
        proteins, fats, carbs, energies = [], [], [], []

        for row in rows:
            codes.append(row.ingredient_code)
            vecs.append(np.frombuffer(row.embedding, dtype="float32"))
            roles.append(row.functional_role)
            proteins.append(row.proteins_100g)
            fats.append(row.fat_100g)
            carbs.append(row.carbohydrates_100g)
            energies.append(row.energy_100g)

        embeddings = np.vstack(vecs).astype("float32")

        # ── Rebuild the in-memory DataFrame ───────────────────────────────
        # Join back the display columns (product_name, sub_category, etc.)
        # that are needed at query time but were not stored in the embedding
        # table (they live in the source tables and don't change).
        base_df = self._load_dataframe(db)

        embed_df = pd.DataFrame({
            "ingredient_code": codes,
            "functional_role":  roles,
            "proteins_100g":    proteins,
            "fat_100g":         fats,
            "carbohydrates_100g": carbs,
            "energy_100g":      energies,
            "_embedding":       list(embeddings),
        }).set_index("ingredient_code")

        # Override the raw nutrition columns with imputed values from the
        # embedding table, then attach the embedding and role columns.
        base_df.update(embed_df[["proteins_100g", "fat_100g",
                                  "carbohydrates_100g", "energy_100g"]])
        base_df["functional_role"] = embed_df["functional_role"]
        base_df["_embedding"]      = embed_df["_embedding"]

        # Drop any ingredients that have no embedding row (shouldn't happen
        # in a healthy DB, but guard against partial seeds).
        self._df = base_df.loc[base_df.index.isin(embed_df.index)]

        # ── Rebuild FAISS index ───────────────────────────────────────────
        self._index = self._build_faiss_index(embeddings)

        self._ready = True
        logger.info("Index loaded from DB. ntotal=%d", self._index.ntotal)
        return True

    def get_substitutes(
        self,
        ingredient_code: str,
        db: Session,
    ) -> SubstituteResult:
        """
        Return the three best substitutes for `ingredient_code`.

        Parameters
        ----------
        ingredient_code : str
            Primary key from the `ingredient` table.
        db : Session
            SQLAlchemy session (used for lazy-build/load fallback).
        """
        if not self._ready:
            logger.warning("Engine not ready; attempting lazy load from DB…")
            if not self.load_index(db):
                logger.info("DB tables empty; triggering lazy build…")
                self.build_index(db)

        df = self._df
        if ingredient_code not in df.index:
            return SubstituteResult(
                query_code=ingredient_code,
                query_name="unknown",
                error=f"Ingredient '{ingredient_code}' not found in index.",
            )

        query_row = df.loc[ingredient_code]
        query_name = str(query_row["product_name"])
        query_role = str(query_row["functional_role"])
        query_vec  = df.at[ingredient_code, "_embedding"]
        query_vec_np = np.array(query_vec, dtype="float32").reshape(1, -1)

        # ── Stage 1: ANN search ────────────────────────────────────────────
        k = min(ANN_K + 1, len(df))  # +1 to skip self
        distances, indices = self._index.search(query_vec_np, k)
        distances = distances[0]
        indices   = indices[0]

        code_list  = df.index.tolist()
        candidates = []
        for dist, idx in zip(distances, indices):
            if idx < 0:
                continue
            code = code_list[idx]
            if code == ingredient_code:
                continue
            cand_role = str(df.at[code, "functional_role"])
            if query_role != "other" and cand_role != "other" and cand_role != query_role:
                continue
            candidates.append((code, float(dist)))

        if not candidates:
            return SubstituteResult(
                query_code=ingredient_code,
                query_name=query_name,
                error="No culinary-valid substitutes found after role filtering.",
            )

        cand_df = df.loc[[c for c, _ in candidates]].copy()
        cand_df["_similarity"] = [d for _, d in candidates]

        # ── Stage 2: Multi-objective scoring ──────────────────────────────
        cand_df = self._add_scores(cand_df)

        budget_row    = cand_df.sort_values("_score_budget",    ascending=False).iloc[0]
        nutrition_row = cand_df.sort_values("_score_nutrition", ascending=False).iloc[0]
        balanced_row  = cand_df.sort_values("_score_balanced",  ascending=False).iloc[0]

        # Diversity: if all three collapse to the same ingredient pull runners-up
        used = {budget_row.name}
        if nutrition_row.name in used:
            remaining = cand_df.drop(index=list(used))
            if not remaining.empty:
                nutrition_row = remaining.sort_values("_score_nutrition", ascending=False).iloc[0]
        used.add(nutrition_row.name)
        if balanced_row.name in used:
            remaining = cand_df.drop(index=list(used))
            if not remaining.empty:
                balanced_row = remaining.sort_values("_score_balanced", ascending=False).iloc[0]

        def _to_slot(row: pd.Series, obj_col: str) -> SubstituteSlot:
            return SubstituteSlot(
                ingredient_code=row.name,
                product_name=str(row.get("product_name", "")),
                brands=row.get("brands"),
                sub_category=row.get("sub_category"),
                retail_price=_nullable_float(row.get("retail_price")),
                nutrition_grade=row.get("nutrition_grade_fr"),
                proteins_100g=_nullable_float(row.get("proteins_100g")),
                fat_100g=_nullable_float(row.get("fat_100g")),
                carbohydrates_100g=_nullable_float(row.get("carbohydrates_100g")),
                energy_100g=_nullable_float(row.get("energy_100g")),
                similarity_score=float(row.get("_similarity", 0.0)),
                objective_score=float(row.get(obj_col, 0.0)),
            )

        return SubstituteResult(
            query_code=ingredient_code,
            query_name=query_name,
            budget=_to_slot(budget_row,    "_score_budget"),
            nutrition=_to_slot(nutrition_row, "_score_nutrition"),
            balanced=_to_slot(balanced_row,   "_score_balanced"),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_dataframe(self, db: Session) -> pd.DataFrame:
        """
        Join ingredient + nutrition + ingredient_price tables into a single
        flat DataFrame indexed by ingredient_code.
        """
        from src.models import Ingredient, Nutrition, IngredientPrice  # noqa: PLC0415

        rows = (
            db.query(
                Ingredient.ingredient_code,
                Ingredient.product_name,
                Ingredient.brands,
                Ingredient.main_category,
                Nutrition.nutrition_grade_fr,
                Nutrition.energy_100g,
                Nutrition.proteins_100g,
                Nutrition.carbohydrates_100g,
                Nutrition.fat_100g,
                IngredientPrice.sub_category,
                IngredientPrice.retail_price,
            )
            .outerjoin(Nutrition,       Nutrition.ingredient_code       == Ingredient.ingredient_code)
            .outerjoin(IngredientPrice, IngredientPrice.ingredient_code == Ingredient.ingredient_code)
            .all()
        )

        df = pd.DataFrame(rows, columns=[
            "ingredient_code", "product_name", "brands", "main_category",
            "nutrition_grade_fr", "energy_100g", "proteins_100g",
            "carbohydrates_100g", "fat_100g",
            "sub_category", "retail_price",
        ]).set_index("ingredient_code")

        df["nutrition_grade_fr"] = df["nutrition_grade_fr"].str.lower().where(
            df["nutrition_grade_fr"].notna(), other=None
        )
        df["functional_role"] = df["sub_category"].apply(_infer_role)
        return df

    def _impute_nutrition(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Impute missing macro values using sub_category-median → global-median.
        """
        macro_cols = ["proteins_100g", "fat_100g", "carbohydrates_100g", "energy_100g"]

        cat_medians: dict[str, dict[str, float]] = {}
        for cat, grp in df.groupby("sub_category", dropna=True):
            cat_medians[str(cat)] = {
                col: grp[col].dropna().median()
                for col in macro_cols
            }

        global_medians = {col: df[col].dropna().median() for col in macro_cols}

        def _fill(row: pd.Series) -> pd.Series:
            cat = str(row.get("sub_category", "")) if row.get("sub_category") else ""
            cat_med = cat_medians.get(cat, {})
            for col in macro_cols:
                if pd.isna(row[col]):
                    row[col] = cat_med.get(col) or global_medians.get(col, 0.0)
            return row

        return df.apply(_fill, axis=1)

    def _build_embeddings(self, df: pd.DataFrame) -> np.ndarray:
        """
        Construct the 388-d hybrid embedding matrix and attach each vector
        to df["_embedding"] for later retrieval.
        """
        if self._model is None:
            logger.info("Loading SentenceTransformer model '%s' …", MODEL_NAME)
            self._model = SentenceTransformer(MODEL_NAME)

        texts = (
            df["product_name"].fillna("").str.strip()
            + " | " + df["sub_category"].fillna("").str.strip()
            + " | " + df["brands"].fillna("").str.strip()
        ).tolist()

        logger.info("Encoding %d ingredient texts…", len(texts))
        semantic_vecs = self._model.encode(
            texts,
            batch_size=256,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        macro_cols = ["proteins_100g", "fat_100g", "carbohydrates_100g", "energy_100g"]
        macro_vals = df[macro_cols].values.astype("float32")

        self._scaler = StandardScaler()
        macro_scaled = self._scaler.fit_transform(macro_vals).astype("float32")
        macro_scaled *= NUTRITION_WEIGHT

        embeddings = np.hstack([semantic_vecs, macro_scaled])  # (N, 388)
        df["_embedding"] = list(embeddings)
        return embeddings

    def _build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """Build and train an IVFFlat FAISS index."""
        dim   = embeddings.shape[1]
        n     = embeddings.shape[0]
        nlist = min(NLIST, max(1, n // 40))

        quantiser = faiss.IndexFlatIP(dim)
        index     = faiss.IndexIVFFlat(quantiser, dim, nlist, faiss.METRIC_INNER_PRODUCT)

        logger.info("Training FAISS IVF index (nlist=%d, dim=%d)…", nlist, dim)
        index.train(embeddings)
        index.add(embeddings)
        index.nprobe = min(32, nlist)
        return index

    def _add_scores(self, cand_df: pd.DataFrame) -> pd.DataFrame:
        """Compute the three objective scores on the candidate DataFrame."""

        prices      = cand_df["retail_price"].astype(float)
        price_range = prices.max() - prices.min()
        cand_df["_score_budget"] = (
            1.0 - (prices - prices.min()) / price_range
            if price_range > 0
            else 0.5
        )

        grade_scores = cand_df["nutrition_grade_fr"].map(
            lambda g: NUTRI_GRADE_MAP.get(str(g).lower() if g else None, 0.3)
        )
        proteins  = cand_df["proteins_100g"].astype(float)
        prot_range = proteins.max() - proteins.min()
        prot_scaled = (
            (proteins - proteins.min()) / prot_range
            if prot_range > 0
            else pd.Series(0.5, index=cand_df.index)
        )

        cand_df["_score_nutrition"] = 0.6 * grade_scores + 0.4 * prot_scaled
        cand_df["_score_balanced"]  = (
            BALANCED_LAMBDA       * cand_df["_score_budget"]
            + (1 - BALANCED_LAMBDA) * cand_df["_score_nutrition"]
        )
        return cand_df


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _nullable_float(val) -> Optional[float]:
    """Return None for NaN/None, else float."""
    if val is None:
        return None
    try:
        f = float(val)
        return None if (f != f) else f   # NaN check: NaN != NaN
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Module-level singleton (imported by main.py)
# ---------------------------------------------------------------------------
engine = IngredientSubstitutionEngine()