"""Generates ingredient substitute pairs from the trained Food2Vec Word2Vec model.

Replaces `python -m food2vec.generate_substitutes_word2vec` (which requires
PyTorch/FoodBERT). This script uses only gensim's most_similar() on the
already-trained Word2Vec model — no torch dependency.

For each ingredient in the vocabulary it finds the top-N most similar
ingredients and writes them as substitute pairs to ingredient_substitutes_raw.csv.

Usage:
    python -m src.scripts.generate_food2vec_substitutes --model <path_to_model.bin>

    # Example:
    python -m src.scripts.generate_food2vec_substitutes \
        --model C:/Users/Priyank/aegis-project-5120/food2vec-repo/food2vec/models/model.bin
"""

from __future__ import annotations

import argparse
import os

import pandas as pd
from gensim.models import Word2Vec

from src.core.config import settings
from src.core.logging import logger

_TOP_N = 5
_MIN_SIMILARITY = 0.40

# Tokens to ignore when building product embeddings
_STOP = {
    "fresh", "dried", "organic", "natural", "premium", "classic", "original",
    "traditional", "rspca", "approved", "australian", "coles", "woolworths",
    "aldi", "free", "range", "gluten", "and", "or", "with", "the", "a", "of",
    "in", "for", "no", "thawed", "frozen", "pack", "each",
}


def _embed_product(name: str, wv) -> "np.ndarray | None":
    """Average Word2Vec vectors for all known tokens in a product name."""
    import re
    import numpy as np
    tokens = [t for t in re.split(r"[^a-z]+", name.lower()) if len(t) > 1 and t not in _STOP]
    vecs = [wv[t] for t in tokens if t in wv]
    if not vecs:
        return None
    v = np.mean(vecs, axis=0).astype(np.float32)
    norm = float(np.linalg.norm(v))
    return v / norm if norm > 0 else v


def generate_substitutes(model_path: str) -> None:
    import numpy as np

    if not os.path.exists(model_path):
        logger.error("Model not found at %s", model_path)
        return

    if not os.path.exists(settings.INGREDIENTS_PRICING_RAW_PATH):
        logger.error("ingredients_pricing_raw.csv not found — run download_dev_data.py first")
        return

    logger.info("Loading Word2Vec model from %s ...", model_path)
    model = Word2Vec.load(model_path)
    wv = model.wv
    logger.info("Vocabulary size: %d", len(wv))

    # Load actual grocery product names from our DB source
    df_pricing = pd.read_csv(settings.INGREDIENTS_PRICING_RAW_PATH)
    df_pricing.columns = df_pricing.columns.str.strip().str.lower()
    product_names: list[str] = df_pricing["name"].dropna().astype(str).unique().tolist()
    logger.info("Computing embeddings for %d grocery products...", len(product_names))

    # Embed every product
    name_to_vec: dict[str, np.ndarray] = {}
    for name in product_names:
        v = _embed_product(name, wv)
        if v is not None:
            name_to_vec[name] = v

    if not name_to_vec:
        logger.error("No product embeddings computed — vocabulary may not overlap with product names")
        return

    logger.info("Embedded %d / %d products", len(name_to_vec), len(product_names))

    # Build matrix for fast cosine similarity
    names = list(name_to_vec.keys())
    matrix = np.stack([name_to_vec[n] for n in names])  # (P, dim)

    records = []
    for i, ing_name in enumerate(names):
        sims = matrix @ name_to_vec[ing_name]  # (P,)
        sims[i] = -1  # exclude self
        top_indices = sims.argsort()[::-1][:_TOP_N]
        for j in top_indices:
            score = float(sims[j])
            if score < _MIN_SIMILARITY:
                break
            records.append({
                "ingredient_name": ing_name,
                "substitute_name": names[j],
                "similarity_score": round(score, 4),
                "reason": "availability",
                "source": "food2vec",
            })

    df = (
        pd.DataFrame(records)
        .drop_duplicates(subset=["ingredient_name", "substitute_name"])
        .sort_values(["ingredient_name", "similarity_score"], ascending=[True, False])
    )

    df.to_csv(settings.INGREDIENT_SUBSTITUTES_RAW_PATH, index=False)
    logger.info(
        "ingredient_substitutes_raw.csv written: %d pairs → %s",
        len(df), settings.INGREDIENT_SUBSTITUTES_RAW_PATH,
    )

    # Also copy the model to our data directory so embedding.py can find it
    dest = settings.FOOD2VEC_MODEL_PATH
    if os.path.abspath(model_path) != os.path.abspath(dest):
        import shutil
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(model_path, dest)
        logger.info("Model copied to %s", dest)

    logger.info(
        "\nNext step — re-seed the database:\n"
        "  cd aegis/backend\n"
        "  python -m src.scripts.fetch_dish_ingredients\n"
        "  python -m src.services.data_seeding"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to trained food2vec model.bin")
    args = parser.parse_args()
    generate_substitutes(args.model)
