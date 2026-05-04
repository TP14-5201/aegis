"""Prepares the Food2Vec training corpus from dishes_raw.csv.

Converts Yummly recipe ingredient lists into the plain-text format expected
by the food2vec training script:
    foodbert/data/train_instructions.txt  (one recipe per line)

Each line contains space-separated ingredient tokens for one recipe, e.g.:
    chicken breast tomato garlic olive oil salt pepper
    beef mince onion carrot celery potato tomato

Usage (run from the backend directory):
    python -m src.scripts.prepare_food2vec_corpus --out <path_to_food2vec_repo>

    # Example:
    python -m src.scripts.prepare_food2vec_corpus --out ../food2vec-repo

The script writes:
    <out>/foodbert/data/train_instructions.txt
"""

from __future__ import annotations

import argparse
import json
import os
import re

import pandas as pd

from src.core.config import settings
from src.core.logging import logger

_QTY_RE = re.compile(
    r"^\s*[\d/½¼¾⅓⅔]+\s*(cup|c\.|tbsp|tsp|tablespoon|teaspoon|oz|lb|g|kg|ml|l"
    r"|pound|ounce|clove|head|bunch|slice|can|jar|pkg|package|medium|large|small"
    r"|piece|pinch|dash|handful)s?\s*",
    re.IGNORECASE,
)

_STOP = {
    "fresh", "dried", "chopped", "diced", "minced", "sliced", "grated",
    "peeled", "crushed", "ground", "cooked", "raw", "frozen", "canned",
    "optional", "to", "taste", "finely", "roughly", "thinly", "and", "or",
    "a", "an", "the", "of", "with", "in", "for", "about",
}


def _tokenize_ingredient(raw: str) -> list[str]:
    raw = _QTY_RE.sub("", raw).strip().lower()
    tokens = re.split(r"[^a-z]+", raw)
    return [t for t in tokens if len(t) > 1 and t not in _STOP]


def prepare_corpus(out_dir: str) -> None:
    if not os.path.exists(settings.DISHES_RAW_PATH):
        logger.error("dishes_raw.csv not found — run download_dev_data.py first")
        return

    df = pd.read_csv(settings.DISHES_RAW_PATH)
    df.columns = df.columns.str.strip().str.lower()

    corpus_dir = os.path.join(out_dir, "foodbert", "data")
    os.makedirs(corpus_dir, exist_ok=True)
    out_path = os.path.join(corpus_dir, "train_instructions.txt")

    lines_written = 0
    skipped = 0

    with open(out_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            try:
                ings = json.loads(row["ingredients"]) if isinstance(row["ingredients"], str) else row["ingredients"]
            except (json.JSONDecodeError, TypeError):
                skipped += 1
                continue
            if not isinstance(ings, list) or not ings:
                skipped += 1
                continue

            tokens: list[str] = []
            for ing in ings:
                tokens.extend(_tokenize_ingredient(str(ing)))

            if tokens:
                f.write(" ".join(tokens) + "\n")
                lines_written += 1

    logger.info(
        "Corpus written: %d recipes → %s  (skipped %d)",
        lines_written, out_path, skipped,
    )
    logger.info(
        "\nNext steps:\n"
        "  cd %s\n"
        "  python -m food2vec.train\n"
        "  python -m food2vec.generate_substitutes_word2vec",
        out_dir,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        required=True,
        help="Path to the cloned food2vec repo root",
    )
    args = parser.parse_args()
    prepare_corpus(args.out)
