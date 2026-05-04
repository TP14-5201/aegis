"""Imports Food2Vec substitute pairs into ingredient_substitutes_raw.csv.

Reads the JSON output from `python -m food2vec.generate_substitutes_word2vec`
(food2vec/data/substitute_pairs_food2vec_text.json) and converts it to the
CSV format expected by data_seeding.seed_ingredient_substitutes().

The similarity score between each pair is computed from the trained Word2Vec
model so it reflects actual semantic distance, not a placeholder.

Usage:
    python -m src.scripts.import_food2vec_substitutes --model-dir <path_to_food2vec_repo>

Output:
    src/data/raw/ingredient_substitutes_raw.csv
    Columns: ingredient_name, substitute_name, similarity_score, reason, source
"""

from __future__ import annotations

import argparse
import json
import os

import pandas as pd

from src.core.config import settings
from src.core.logging import logger
from src.services.embedding import food2vec


def import_substitutes(model_dir: str) -> None:
    json_path = os.path.join(model_dir, "food2vec", "data", "substitute_pairs_food2vec_text.json")

    if not os.path.exists(json_path):
        logger.error(
            "Substitute pairs not found at %s\n"
            "Run: cd %s && python -m food2vec.generate_substitutes_word2vec",
            json_path, model_dir,
        )
        return

    with open(json_path, encoding="utf-8") as f:
        pairs: list[list[str]] = json.load(f)

    logger.info("Loaded %d substitute pairs from %s", len(pairs), json_path)

    records = []
    for pair in pairs:
        if len(pair) != 2:
            continue
        ing, sub = pair[0].strip().lower(), pair[1].strip().lower()
        if not ing or not sub or ing == sub:
            continue

        # Compute similarity from the Food2Vec model if available
        if food2vec.available:
            v_ing = food2vec.embed(ing)
            v_sub = food2vec.embed(sub)
            if v_ing is not None and v_sub is not None:
                score = round(float(food2vec._cosine(v_ing, v_sub)), 4)
            else:
                score = None
        else:
            score = None

        records.append({
            "ingredient_name": ing,
            "substitute_name": sub,
            "similarity_score": score,
            "reason": "availability",
            "source": "food2vec",
        })

    df = pd.DataFrame(records).drop_duplicates(subset=["ingredient_name", "substitute_name"])
    df.to_csv(settings.INGREDIENT_SUBSTITUTES_RAW_PATH, index=False)

    logger.info(
        "ingredient_substitutes_raw.csv written: %d pairs → %s",
        len(df), settings.INGREDIENT_SUBSTITUTES_RAW_PATH,
    )
    logger.info(
        "\nNext step — re-seed the database:\n"
        "  python -m src.services.data_seeding"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-dir",
        required=True,
        help="Path to the cloned food2vec repo root",
    )
    args = parser.parse_args()
    import_substitutes(args.model_dir)
