import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock, call

from src.services.data_seeding import (
    seed_simple,
    download_dataset,
    seed_ingredients,
    seed_dishes,
    seed_ingredient_nutrients,
    seed_ingredient_substitutes,
    seed_dish_ingredients,
    _infer_dietary_flags
)
from src.core.config import settings

# ---------------------------------------------------------------------------
# Shared helpers & fixtures
# ---------------------------------------------------------------------------

def make_sample_df(n: int = 2) -> pd.DataFrame:
    rows = [{"id": i, "name": f"Item {i}"} for i in range(n)]
    return pd.DataFrame(rows)

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.query.return_value.delete.return_value = None
    db.bulk_save_objects.return_value = None
    db.commit.return_value = None
    db.rollback.return_value = None
    # For db.add and db.flush
    db.add.return_value = None
    db.flush.return_value = None
    return db

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.__name__ = "MockModel"
    model.__tablename__ = "mock_model"
    return model

# ---------------------------------------------------------------------------
# seed_simple
# ---------------------------------------------------------------------------

class TestSeedSimple:
    def test_queries_and_deletes_the_given_model(self, mock_db, mock_model):
        df = make_sample_df()
        seed_simple(mock_db, df, mock_model)
        mock_db.query.assert_called_once_with(mock_model)
        mock_db.query.return_value.delete.assert_called_once()

    def test_bulk_saves_correct_number_of_objects(self, mock_db, mock_model):
        seed_simple(mock_db, make_sample_df(n=3), mock_model)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 3

    def test_commits_after_successful_insert(self, mock_db, mock_model):
        seed_simple(mock_db, make_sample_df(), mock_model)
        mock_db.commit.assert_called_once()

    def test_rollback_on_bulk_save_exception(self, mock_db, mock_model):
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            seed_simple(mock_db, make_sample_df(), mock_model)
        mock_db.rollback.assert_called_once()

# ---------------------------------------------------------------------------
# Seed functions tests
# ---------------------------------------------------------------------------

class TestSeedFunctions:
    def test_seed_ingredients(self, mock_db):
        df = pd.DataFrame([{"name": "Apple", "pack_grams": 100, "price_aud": 2.0, "benefit_tags": '["healthy"]'}])
        # We need to simulate db.add modifying the object so it has an id
        def side_effect_add(obj):
            obj.id = 1
        mock_db.add.side_effect = side_effect_add
        
        name_to_id = seed_ingredients(mock_db, df)
        assert mock_db.add.called
        assert mock_db.commit.called
        assert "apple" in name_to_id
        
    def test_infer_dietary_flags(self):
        flags = _infer_dietary_flags(["apple", "banana"])
        assert "vegan" in flags
        assert "vegetarian" in flags
        flags_meat = _infer_dietary_flags(["beef", "milk"])
        assert "vegan" not in flags_meat

    def test_seed_dishes(self, mock_db):
        df = pd.DataFrame([{"name": "Fruit Salad", "ingredients": '["apple", "banana"]', "base_servings": 4}])
        def side_effect_add(obj):
            obj.id = 1
        mock_db.add.side_effect = side_effect_add

        name_to_id = seed_dishes(mock_db, df)
        assert mock_db.add.called
        assert mock_db.commit.called
        assert "fruit salad" in name_to_id

    def test_seed_ingredient_nutrients(self, mock_db):
        df = pd.DataFrame([{"ingredient_name": "apple", "nutrient_name": "vitamin c", "amount_per_100g": 10, "unit": "mg"}])
        seed_ingredient_nutrients(mock_db, df, {"apple": 1})
        assert mock_db.bulk_save_objects.called
        assert mock_db.commit.called

    def test_seed_ingredient_substitutes(self, mock_db):
        df = pd.DataFrame([{"ingredient_name": "apple", "substitute_name": "pear", "similarity_score": 0.8, "reason": "taste", "source": "test"}])
        seed_ingredient_substitutes(mock_db, df, {"apple": 1, "pear": 2})
        assert mock_db.bulk_save_objects.called
        assert mock_db.commit.called

    def test_seed_dish_ingredients(self, mock_db):
        df = pd.DataFrame([{"dish_name": "salad", "ingredient_name": "apple", "quantity_g": 100, "is_optional": False}])
        seed_dish_ingredients(mock_db, df, {"salad": 1}, {"apple": 2})
        assert mock_db.bulk_save_objects.called
        assert mock_db.commit.called

# ---------------------------------------------------------------------------
# download_dataset
# ---------------------------------------------------------------------------

class TestDownloadDataset:
    def test_downloads_when_all_files_missing(self):
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy") as mock_save, \
             patch("src.services.data_seeding.fetch_yummly_dishes") as mock_yummly, \
             patch("src.services.data_seeding.fetch_vic_grocery_ingredients") as mock_vic, \
             patch("src.services.data_seeding.fetch_miskg_substitutes") as mock_misk:
            mock_yummly.return_value = pd.DataFrame([{"name": "test"}])
            mock_misk.return_value = pd.DataFrame([{"ingredient_name": "test"}])
            download_dataset()
            mock_save.assert_called_once()
            mock_yummly.assert_called_once()
            mock_vic.assert_called_once()
            mock_misk.assert_called_once()

    def test_does_not_download_when_files_present(self):
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy") as mock_save, \
             patch("src.services.data_seeding._fetch_nutrients") as mock_nutrients:
            download_dataset()
            mock_save.assert_not_called()
            mock_nutrients.assert_called_once()