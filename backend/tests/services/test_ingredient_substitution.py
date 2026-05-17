import numpy as np
import pandas as pd
import pytest
import pickle
import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.services import ingredient_substitution as module
from src.services.ingredient_substitution import IngredientSubstitutionEngine


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ready_engine(n: int = 10) -> IngredientSubstitutionEngine:
    """Return an engine with _ready=True and a minimal in-memory index."""
    engine = IngredientSubstitutionEngine()

    codes = [f"CODE_{i:04d}" for i in range(n)]
    vecs = np.random.rand(n, 388).astype("float32")
    # L2-normalise so inner product = cosine similarity
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    vecs = vecs / np.maximum(norms, 1e-8)

    import faiss
    index = faiss.IndexFlatIP(388)
    index.add(vecs)

    df = pd.DataFrame({"ingredient_code": codes}).set_index("ingredient_code")

    mock_model = MagicMock()
    mock_model.encode = MagicMock(
        side_effect=lambda texts, normalize_embeddings=True: np.random.rand(len(texts), 384).astype("float32")
    )

    engine._model = mock_model
    engine._index = index
    engine._df = df
    engine._ready = True
    return engine


# ---------------------------------------------------------------------------
# find_similar_to_text
# ---------------------------------------------------------------------------

class TestFindSimilarToText:
    def test_engine_not_ready_returns_empty(self):
        engine = IngredientSubstitutionEngine()
        assert engine._ready is False
        result = engine.find_similar_to_text("I love seafood")
        assert result == {}

    def test_returns_dict_of_codes_to_scores(self):
        engine = _make_ready_engine(n=20)
        result = engine.find_similar_to_text("high protein meals", top_k=10)
        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result)
        assert all(isinstance(v, float) for v in result.values())

    def test_all_scores_non_negative(self):
        engine = _make_ready_engine(n=20)
        result = engine.find_similar_to_text("seafood", top_k=10)
        assert all(v >= 0.0 for v in result.values())

    def test_result_count_respects_top_k(self):
        engine = _make_ready_engine(n=20)
        result = engine.find_similar_to_text("vegetables", top_k=5)
        assert len(result) <= 5

    def test_top_k_larger_than_index_capped(self):
        engine = _make_ready_engine(n=8)
        result = engine.find_similar_to_text("anything", top_k=200)
        assert len(result) <= 8

    def test_query_vector_shape_is_388d(self):
        engine = _make_ready_engine(n=10)
        captured = {}
        original_search = engine._index.search
        def intercepted_search(vec, k):
            captured["shape"] = vec.shape
            return original_search(vec, k)
        engine._index.search = intercepted_search
        engine.find_similar_to_text("muscle gain", top_k=5)
        assert captured["shape"] == (1, 388)

    def test_text_truncated_to_300_chars(self):
        engine = _make_ready_engine(n=10)
        long_text = "x" * 500
        engine.find_similar_to_text(long_text, top_k=5)
        call_args = engine._model.encode.call_args
        encoded_text = call_args[0][0][0]
        assert len(encoded_text) <= 300

    def test_returns_ingredient_codes_from_index(self):
        engine = _make_ready_engine(n=10)
        result = engine.find_similar_to_text("protein", top_k=5)
        valid_codes = set(engine._df.index.tolist())
        assert all(code in valid_codes for code in result)


class FakeIndex:
    def __init__(self, distances, indices):
        self.distances = np.array([distances], dtype="float32")
        self.indices = np.array([indices], dtype="int64")
        self.ntotal = len(indices)

    def search(self, vec, k):
        return self.distances[:, :k], self.indices[:, :k]


def _substitution_df():
    vecs = [np.full(388, i, dtype="float32") for i in range(5)]
    return pd.DataFrame(
        {
            "ingredient_code": ["query", "cheap", "healthy", "balanced", "other_role"],
            "product_name": ["Original", "Budget Pick", "Nutri Pick", "Balanced Pick", "Wrong Role"],
            "sub_category": ["pasta", "pasta", "pasta", "pasta", "dairy"],
            "health_benefits": [None, ["low cost"], ["protein"], ["steady"], None],
            "retail_price": [5.0, 1.0, 4.0, 2.0, 0.5],
            "nutrition_grade_fr": ["c", "d", "a", "b", "a"],
            "proteins_100g": [5.0, 4.0, 20.0, 12.0, 30.0],
            "fat_100g": [1.0, 2.0, 3.0, 4.0, 5.0],
            "carbohydrates_100g": [40.0, 41.0, 42.0, 43.0, 44.0],
            "energy_100g": [190.0, 200.0, 210.0, 220.0, 230.0],
            "functional_role": ["carb", "carb", "carb", "carb", "dairy_protein"],
            "_embedding": vecs,
        }
    ).set_index("ingredient_code")


class TestRoleAndHelpers:
    @pytest.mark.parametrize(
        ("sub_category", "expected"),
        [
            (None, "other"),
            (123, "other"),
            ("Fresh chicken breast", "protein"),
            ("Greek yoghurt", "dairy_protein"),
            ("Red lentil", "plant_protein"),
            ("Wholegrain pasta", "carb"),
            ("Leafy vegetable", "vegetable"),
            ("Citrus fruit", "fruit"),
            ("Olive oil", "fat"),
            ("Ketchup", "flavour"),
            ("Soft drink", "beverage"),
            ("mystery aisle", "other"),
        ],
    )
    def test_infer_role(self, sub_category, expected):
        assert module._infer_role(sub_category) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [(None, None), (float("nan"), None), ("bad", None), ("3.5", 3.5)],
    )
    def test_nullable_float(self, value, expected):
        assert module._nullable_float(value) == expected


class TestScoringAndEmbeddings:
    def test_add_scores_uses_min_max_and_grade_mapping(self):
        engine = IngredientSubstitutionEngine()
        df = pd.DataFrame(
            {
                "retail_price": [1.0, 3.0],
                "nutrition_grade_fr": ["a", "e"],
                "proteins_100g": [10.0, 20.0],
            },
            index=["cheap", "protein"],
        )

        scored = engine._add_scores(df)

        assert scored.at["cheap", "_score_budget"] == pytest.approx(1.0)
        assert scored.at["protein", "_score_budget"] == pytest.approx(0.0)
        assert scored.at["cheap", "_score_nutrition"] == pytest.approx(0.6)
        assert scored.at["protein", "_score_nutrition"] == pytest.approx(0.52)

    def test_add_scores_handles_equal_prices_and_proteins(self):
        engine = IngredientSubstitutionEngine()
        df = pd.DataFrame(
            {
                "retail_price": [2.0, 2.0],
                "nutrition_grade_fr": [None, "z"],
                "proteins_100g": [5.0, 5.0],
            },
            index=["one", "two"],
        )

        scored = engine._add_scores(df)

        assert scored["_score_budget"].tolist() == [0.5, 0.5]
        assert scored["_score_nutrition"].tolist() == pytest.approx([0.38, 0.38])

    def test_impute_nutrition_prefers_category_then_global_medians(self):
        engine = IngredientSubstitutionEngine()
        df = pd.DataFrame(
            {
                "sub_category": ["pasta", "pasta", None],
                "proteins_100g": [10.0, np.nan, np.nan],
                "fat_100g": [1.0, 3.0, np.nan],
                "carbohydrates_100g": [20.0, np.nan, 50.0],
                "energy_100g": [100.0, np.nan, 200.0],
            }
        )

        filled = engine._impute_nutrition(df)

        assert filled.loc[1, "proteins_100g"] == 10.0
        assert filled.loc[1, "carbohydrates_100g"] == 20.0
        assert filled.loc[2, "fat_100g"] == 2.0

    def test_build_embeddings_uses_existing_model_and_attaches_vectors(self):
        engine = IngredientSubstitutionEngine()
        engine._model = MagicMock()
        engine._model.encode.return_value = np.ones((2, 384), dtype="float32")
        df = pd.DataFrame(
            {
                "product_name": [" Apple ", None],
                "sub_category": ["fruit", "grain"],
                "proteins_100g": [1.0, 2.0],
                "fat_100g": [0.0, 1.0],
                "carbohydrates_100g": [10.0, 20.0],
                "energy_100g": [50.0, 100.0],
            }
        )

        embeddings = engine._build_embeddings(df)

        assert embeddings.shape == (2, 388)
        assert "_embedding" in df
        engine._model.encode.assert_called_once()
        assert engine._model.encode.call_args.args[0] == ["Apple | fruit", " | grain"]

    def test_build_embeddings_lazy_loads_model(self):
        engine = IngredientSubstitutionEngine()
        fake_model = MagicMock()
        fake_model.encode.return_value = np.ones((1, 384), dtype="float32")
        df = pd.DataFrame(
            {
                "product_name": ["Rice"],
                "sub_category": ["grain"],
                "proteins_100g": [1.0],
                "fat_100g": [0.0],
                "carbohydrates_100g": [20.0],
                "energy_100g": [100.0],
            }
        )

        with patch("src.services.ingredient_substitution.SentenceTransformer", return_value=fake_model):
            assert engine._build_embeddings(df).shape == (1, 388)

    def test_build_faiss_index_trains_and_adds_vectors(self):
        engine = IngredientSubstitutionEngine()
        embeddings = np.random.rand(4, 8).astype("float32")

        index = engine._build_faiss_index(embeddings)

        assert index.ntotal == 4
        assert index.nprobe == 1


class TestGetSubstitutes:
    def test_get_substitutes_lazily_builds_when_load_fails(self):
        engine = IngredientSubstitutionEngine()
        ready_engine = IngredientSubstitutionEngine()
        ready_engine._df = _substitution_df()
        ready_engine._index = FakeIndex([1, 0.9, 0.8, 0.7], [0, 1, 2, 3])
        ready_engine._ready = True

        def build_index(db):
            engine._df = ready_engine._df
            engine._index = ready_engine._index
            engine._ready = True

        with patch.object(engine, "load_index", return_value=False), \
             patch.object(engine, "build_index", side_effect=build_index) as build:
            result = engine.get_substitutes("query", MagicMock())

        build.assert_called_once()
        assert result.error is None

    def test_get_substitutes_returns_not_found_error(self):
        engine = IngredientSubstitutionEngine()
        engine._ready = True
        engine._df = _substitution_df()

        result = engine.get_substitutes("missing", MagicMock())

        assert result.query_name == "unknown"
        assert "not found" in result.error

    def test_get_substitutes_filters_roles_and_returns_diverse_slots(self):
        engine = IngredientSubstitutionEngine()
        engine._ready = True
        engine._df = _substitution_df()
        engine._index = FakeIndex([1.0, 0.95, 0.9, 0.85, 0.8], [0, 4, 1, 2, 3])

        result = engine.get_substitutes("query", MagicMock())

        assert result.error is None
        assert result.query_name == "Original"
        assert result.budget.ingredient_code == "cheap"
        assert result.nutrition.ingredient_code == "healthy"
        assert result.balanced.ingredient_code == "balanced"
        assert result.budget.retail_price == 1.0
        assert result.budget.health_benefits == ["low cost"]

    def test_get_substitutes_returns_error_when_no_candidates_survive(self):
        engine = IngredientSubstitutionEngine()
        engine._ready = True
        engine._df = _substitution_df()
        engine._index = FakeIndex([1.0, 0.9, -1.0], [0, 4, -1])

        result = engine.get_substitutes("query", MagicMock())

        assert "No culinary-valid substitutes" in result.error


class QueryStub:
    def __init__(self, first_value=None, all_value=None):
        self.first_value = first_value
        self.all_value = all_value or []
        self.deleted = False

    def filter_by(self, **kwargs):
        return self

    def first(self):
        return self.first_value

    def all(self):
        return self.all_value

    def delete(self):
        self.deleted = True


class DbStub:
    def __init__(self, meta=None, rows=None, fail_commit=False):
        self.meta_query = QueryStub(meta)
        self.embedding_query = QueryStub(all_value=rows or [])
        self.saved_objects = []
        self.added = []
        self.committed = False
        self.rolled_back = False
        self.fail_commit = fail_commit

    def query(self, model):
        if model.__name__ in {"SubstitutionMeta", "StubSubstitutionMeta"}:
            return self.meta_query
        return self.embedding_query

    def bulk_save_objects(self, objects):
        self.saved_objects = objects

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        if self.fail_commit:
            raise RuntimeError("commit failed")
        self.committed = True

    def rollback(self):
        self.rolled_back = True


class StubIngredientEmbedding:
    __name__ = "IngredientEmbedding"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class StubSubstitutionMeta:
    __name__ = "SubstitutionMeta"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def models_stub():
    return types.SimpleNamespace(
        IngredientEmbedding=StubIngredientEmbedding,
        SubstitutionMeta=StubSubstitutionMeta,
    )


class TestBuildAndLoadIndex:
    def test_load_index_returns_false_without_scaler_meta(self):
        engine = IngredientSubstitutionEngine()

        with patch.dict(sys.modules, {"src.models": models_stub()}):
            assert engine.load_index(DbStub(meta=None)) is False

    def test_load_index_returns_false_without_embedding_rows(self):
        engine = IngredientSubstitutionEngine()
        db = DbStub(meta=SimpleNamespace(value=pickle.dumps("scaler")), rows=[])

        with patch.dict(sys.modules, {"src.models": models_stub()}):
            assert engine.load_index(db) is False
        assert engine._scaler == "scaler"

    def test_load_index_reconstructs_dataframe_and_index(self):
        engine = IngredientSubstitutionEngine()
        rows = [
            SimpleNamespace(
                ingredient_code="a",
                embedding=np.ones(3, dtype="float32").tobytes(),
                functional_role="carb",
                proteins_100g=1.0,
                fat_100g=2.0,
                carbohydrates_100g=3.0,
                energy_100g=4.0,
            )
        ]
        db = DbStub(meta=SimpleNamespace(value=pickle.dumps("scaler")), rows=rows)
        base_df = pd.DataFrame(
            {
                "ingredient_code": ["a", "b"],
                "product_name": ["A", "B"],
                "sub_category": ["grain", "grain"],
                "retail_price": [1.0, 2.0],
                "nutrition_grade_fr": ["a", "b"],
                "proteins_100g": [9.0, 9.0],
                "fat_100g": [9.0, 9.0],
                "carbohydrates_100g": [9.0, 9.0],
                "energy_100g": [9.0, 9.0],
            }
        ).set_index("ingredient_code")

        with patch.object(engine, "_load_dataframe", return_value=base_df), \
             patch.object(engine, "_build_faiss_index", return_value=SimpleNamespace(ntotal=1)) as build, \
             patch.dict(sys.modules, {"src.models": models_stub()}):
            assert engine.load_index(db) is True

        build.assert_called_once()
        assert engine._ready is True
        assert engine._df.index.tolist() == ["a"]
        assert engine._df.at["a", "proteins_100g"] == 1.0

    def test_build_index_persists_embeddings_and_scaler(self):
        engine = IngredientSubstitutionEngine()
        df = _substitution_df().iloc[:2].copy()
        embeddings = np.vstack(df["_embedding"].to_numpy()).astype("float32")
        engine._scaler = "scaler"
        db = DbStub()

        with patch.object(engine, "_impute_nutrition", return_value=df), \
             patch.object(engine, "_build_embeddings", return_value=embeddings), \
             patch.object(engine, "_build_faiss_index", return_value=SimpleNamespace(ntotal=2)), \
             patch.dict(sys.modules, {"src.models": models_stub()}):
            engine.build_index(db, df=df)

        assert len(db.saved_objects) == 2
        assert db.committed is True
        assert engine._ready is True

    def test_build_index_rolls_back_on_persist_error(self):
        engine = IngredientSubstitutionEngine()
        df = _substitution_df().iloc[:1].copy()
        embeddings = np.vstack(df["_embedding"].to_numpy()).astype("float32")
        engine._scaler = "scaler"
        db = DbStub(fail_commit=True)

        with patch.object(engine, "_impute_nutrition", return_value=df), \
             patch.object(engine, "_build_embeddings", return_value=embeddings), \
             patch.object(engine, "_build_faiss_index", return_value=SimpleNamespace(ntotal=1)), \
             patch.dict(sys.modules, {"src.models": models_stub()}), \
             pytest.raises(RuntimeError):
            engine.build_index(db, df=df)

        assert db.rolled_back is True
