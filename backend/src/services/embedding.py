"""Food2Vec embedding service for semantic ingredient matching.

Uses pre-trained food word vectors (gensim KeyedVectors format).
Vectors for each ingredient are computed by averaging token vectors,
then cosine similarity is used to rank candidates.

When the model file is absent the service falls back to a Jaccard
token-overlap heuristic so the rest of the pipeline keeps working.

Training the model
------------------
1. Clone https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution

2. Prepare the corpus from our Yummly data:
       python -m src.scripts.prepare_food2vec_corpus --out <path_to_repo>

3. Train:
       cd <path_to_repo>
       python -m food2vec.train

4. Generate substitutes:
       python -m food2vec.generate_substitutes_word2vec

5. Copy the model into our data directory:
       cp <path_to_repo>/food2vec/models/model.bin src/data/raw/food2vec.bin

6. Import the substitute pairs:
       python -m src.scripts.import_food2vec_substitutes --model-dir <path_to_repo>

The service accepts both the gensim Word2Vec native .bin and a .kv (KeyedVectors)
file — set FOOD2VEC_MODEL_PATH in config to whichever you have.
"""

from __future__ import annotations

import os
import re
from typing import Optional

import numpy as np

from src.core.config import settings
from src.core.logging import logger

_STOP_TOKENS = {
    "fresh", "dried", "chopped", "diced", "minced", "sliced", "grated",
    "peeled", "crushed", "ground", "cooked", "raw", "frozen", "canned",
    "organic", "natural", "premium", "classic", "original", "traditional",
    "rspca", "approved", "australian", "coles", "woolworths", "aldi",
    "and", "or", "with", "the", "a", "of", "in", "for", "no",
}

_QTY_RE = re.compile(
    r"\b\d[\d.,]*\s*(g|kg|ml|l|mg|mcg|iu|oz|lb|cup|tbsp|tsp|pack|pk|each|x)?\b",
    re.IGNORECASE,
)


def _tokenize(text: str) -> list[str]:
    text = _QTY_RE.sub("", text.lower())
    tokens = [t for t in re.split(r"[^a-z]+", text) if len(t) > 1 and t not in _STOP_TOKENS]
    return tokens


class Food2VecService:
    """Singleton wrapper around a gensim KeyedVectors food model."""

    def __init__(self) -> None:
        self._kv = None
        self._dim: int = 0
        self._load()

    def _load(self) -> None:
        path = getattr(settings, "FOOD2VEC_MODEL_PATH", "")
        if not path or not os.path.exists(path):
            logger.warning(
                "Food2Vec model not found at '%s'. "
                "Falling back to token-overlap matching. "
                "Set FOOD2VEC_MODEL_PATH in config once the model is downloaded.",
                path,
            )
            return
        try:
            self._kv = self._load_model(path)
            self._dim = self._kv.vector_size
            logger.info("Food2Vec loaded: %d vectors, dim=%d", len(self._kv), self._dim)
        except Exception as exc:
            logger.error("Failed to load Food2Vec model from '%s': %s", path, exc)

    @staticmethod
    def _load_model(path: str):
        """Load gensim Word2Vec .bin or KeyedVectors .kv — whichever format is present."""
        from gensim.models import Word2Vec, KeyedVectors
        if path.endswith(".kv"):
            return KeyedVectors.load(path, mmap="r")
        # Gensim native Word2Vec save (model.bin from food2vec.train)
        try:
            return Word2Vec.load(path).wv
        except Exception:
            # Fallback: word2vec-format binary (e.g. Google News vectors)
            return KeyedVectors.load_word2vec_format(path, binary=True)

    @property
    def available(self) -> bool:
        return self._kv is not None

    # ------------------------------------------------------------------
    # Embedding helpers
    # ------------------------------------------------------------------

    def embed(self, text: str) -> Optional[np.ndarray]:
        """Return mean-pooled vector for a food phrase, or None if no tokens hit."""
        if self._kv is None:
            return None
        vecs = [self._kv[t] for t in _tokenize(text) if t in self._kv]
        if not vecs:
            return None
        v = np.mean(vecs, axis=0).astype(np.float32)
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))  # vectors are already L2-normalised

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    def batch_match(
        self,
        queries: list[str],
        candidates: list[str],
        threshold: float = 0.60,
    ) -> dict[str, Optional[str]]:
        """Match every query to its best candidate above threshold.

        Uses vectorised matrix multiplication when the model is loaded,
        making it fast even for large batches (20 k queries × 1 k products
        runs in a few seconds on CPU).
        """
        if self._kv is not None:
            return self._embed_match(queries, candidates, threshold)
        return self._token_overlap_batch(queries, candidates, threshold=0.35)

    def _embed_match(
        self,
        queries: list[str],
        candidates: list[str],
        threshold: float,
    ) -> dict[str, Optional[str]]:
        # Pre-embed candidates → (C, dim) matrix
        cand_vecs: list[np.ndarray] = []
        valid_cands: list[str] = []
        for c in candidates:
            v = self.embed(c)
            if v is not None:
                cand_vecs.append(v)
                valid_cands.append(c)

        if not cand_vecs:
            return {q: None for q in queries}

        C = np.stack(cand_vecs)  # (C, dim)

        results: dict[str, Optional[str]] = {}
        for q in queries:
            q_vec = self.embed(q)
            if q_vec is None:
                results[q] = self._token_overlap_match(q, candidates, threshold=0.35)
                continue
            sims = C @ q_vec  # (C,)
            best_idx = int(np.argmax(sims))
            results[q] = valid_cands[best_idx] if sims[best_idx] >= threshold else None
        return results

    def _token_overlap_match(
        self, query: str, candidates: list[str], threshold: float
    ) -> Optional[str]:
        q_tokens = set(_tokenize(query))
        if not q_tokens:
            return None
        best: Optional[str] = None
        best_score = threshold
        for cand in candidates:
            c_tokens = set(_tokenize(cand))
            if not c_tokens:
                continue
            score = len(q_tokens & c_tokens) / len(q_tokens | c_tokens)
            if score > best_score:
                best_score = score
                best = cand
        return best

    def _token_overlap_batch(
        self,
        queries: list[str],
        candidates: list[str],
        threshold: float,
    ) -> dict[str, Optional[str]]:
        return {q: self._token_overlap_match(q, candidates, threshold) for q in queries}


# Module-level singleton — imported by scripts and services
food2vec = Food2VecService()
