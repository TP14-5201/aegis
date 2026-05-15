import numpy as np
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

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
