import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, call

from src.services.data_seeding import (
    seed_support_services,
    download_dataset,
    load_dataset,
)
from src.core.config import settings


# ---------------------------------------------------------------------------
# Shared helpers & fixtures
# ---------------------------------------------------------------------------

def make_sample_df(n: int = 2) -> pd.DataFrame:
    """Minimal wrangled DataFrame matching the SupportService schema."""
    rows = [
        {
            "name": f"Service {i}",
            "description": f"Description {i}",
            "target_audience": "Everyone",
            "address": f"{i} Main St",
            "suburb": "Melbourne",
            "primary_phone": "0312345678",
            "phone_display": "Phone 1: 0312345678",
            "email": np.nan,
            "website": "https://example.com",
            "social_media": np.nan,
            "opening_hours": {"monday": "09:00am - 05:00pm"},
            "cost": "Free",
            "tram_routes": "1, 2",
            "bus_routes": "901",
            "nearest_train_station": "Flinders Street",
            "categories": ["Food"],
            "longitude": 144.9631,
            "latitude": -37.8136,
            "source": "City of Melbourne",
        }
        for i in range(n)
    ]
    return pd.DataFrame(rows)


# Sample DataFrames for each dataset type (minimal schema, distinct enough to
# identify which loader produced which result in tuple-unpacking assertions).
EMERGENCY_DF      = make_sample_df(n=2)
FOOD_DF           = pd.DataFrame({"indicator": ["food"], "estimate_pct": [10.0]})
VIC_DF            = pd.DataFrame({"vicgov_region": ["South East"], "geometry": ["POLYGON(...)"]})
VICLGA_DF         = pd.DataFrame({"lga_name": ["Melbourne"], "geometry": ["POLYGON(...)"]})


@pytest.fixture
def mock_db():
    """A mock SQLAlchemy Session with all required methods pre-configured."""
    db = MagicMock()
    db.query.return_value.delete.return_value = None
    db.bulk_save_objects.return_value = None
    db.commit.return_value = None
    db.rollback.return_value = None
    return db


@pytest.fixture
def mock_model():
    """A minimal mock ORM model class."""
    model = MagicMock()
    model.__name__ = "MockModel"
    return model


# ---------------------------------------------------------------------------
# seed_support_services
# ---------------------------------------------------------------------------

class TestSeedSupportServices:
    """
    seed_support_services(db, df, model) requires THREE arguments.
    All original tests called it with two — they would all TypeError immediately.
    Fixed by passing `mock_model` as the third argument throughout.
    """

    def test_queries_and_deletes_the_given_model(self, mock_db, mock_model):
        """Tests that the correct model is queried and its rows are deleted."""
        df = make_sample_df()
        seed_support_services(mock_db, df, mock_model)
        mock_db.query.assert_called_once_with(mock_model)
        mock_db.query.return_value.delete.assert_called_once()

    def test_deletes_before_insert(self, mock_db, mock_model):
        """Tests that delete precedes bulk_save to prevent duplicates on re-runs."""
        call_order = []
        mock_db.query.return_value.delete.side_effect = lambda: call_order.append("delete")
        mock_db.bulk_save_objects.side_effect = lambda objs: call_order.append("bulk_save")
        df = make_sample_df()
        seed_support_services(mock_db, df, mock_model)
        assert call_order == ["delete", "bulk_save"]

    def test_bulk_saves_correct_number_of_objects(self, mock_db, mock_model):
        """Tests that the correct number of model instances are bulk-saved."""
        df = make_sample_df(n=3)
        seed_support_services(mock_db, df, mock_model)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 3

    def test_model_instantiated_from_each_row(self, mock_db, mock_model):
        """Tests that the model constructor is called once per DataFrame row."""
        df = make_sample_df(n=4)
        seed_support_services(mock_db, df, mock_model)
        assert mock_model.call_count == 4

    def test_commits_after_successful_insert(self, mock_db, mock_model):
        """Tests that db.commit() is called after a successful bulk save."""
        df = make_sample_df()
        seed_support_services(mock_db, df, mock_model)
        mock_db.commit.assert_called_once()

    def test_rollback_on_bulk_save_exception(self, mock_db, mock_model):
        """Tests that db.rollback() is called when bulk_save_objects raises."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with pytest.raises(Exception):
            seed_support_services(mock_db, df, mock_model)
        mock_db.rollback.assert_called_once()

    def test_rollback_on_delete_exception(self, mock_db, mock_model):
        """Tests that db.rollback() is called when the initial delete raises."""
        mock_db.query.return_value.delete.side_effect = Exception("Delete failed")
        df = make_sample_df()
        with pytest.raises(Exception):
            seed_support_services(mock_db, df, mock_model)
        mock_db.rollback.assert_called_once()

    def test_reraises_exception_after_rollback(self, mock_db, mock_model):
        """Tests that the original exception is re-raised after rollback."""
        mock_db.bulk_save_objects.side_effect = RuntimeError("Unexpected failure")
        df = make_sample_df()
        with pytest.raises(RuntimeError, match="Unexpected failure"):
            seed_support_services(mock_db, df, mock_model)

    def test_does_not_commit_on_exception(self, mock_db, mock_model):
        """Tests that db.commit() is NOT called when an exception occurs."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with pytest.raises(Exception):
            seed_support_services(mock_db, df, mock_model)
        mock_db.commit.assert_not_called()

    def test_returns_none(self, mock_db, mock_model):
        """Tests that seed_support_services returns None (it is a void function)."""
        df = make_sample_df()
        result = seed_support_services(mock_db, df, mock_model)
        assert result is None

    def test_logs_start_with_record_count(self, mock_db, mock_model):
        """Tests that the start log includes the number of records to be inserted."""
        df = make_sample_df(n=5)
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, df, mock_model)
        mock_logger.info.assert_any_call("Starting database seed with 5 records...")

    def test_logs_success_with_inserted_count(self, mock_db, mock_model):
        """Tests that a success log is emitted with the count of inserted records."""
        df = make_sample_df(n=2)
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, df, mock_model)
        mock_logger.info.assert_any_call(
            "Database seeding completed successfully! Inserted 2 records."
        )

    def test_logs_error_on_exception(self, mock_db, mock_model):
        """Tests that an error is logged when an exception occurs."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with patch("src.services.data_seeding.logger") as mock_logger:
            with pytest.raises(Exception):
                seed_support_services(mock_db, df, mock_model)
        mock_logger.error.assert_called_once()

    def test_empty_dataframe_still_deletes_and_commits(self, mock_db, mock_model):
        """Tests that an empty DataFrame still triggers delete and commit."""
        df = make_sample_df(n=0)
        seed_support_services(mock_db, df, mock_model)
        mock_db.query.return_value.delete.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_empty_dataframe_bulk_saves_zero_objects(self, mock_db, mock_model):
        """Tests that an empty DataFrame passes an empty list to bulk_save_objects."""
        df = make_sample_df(n=0)
        seed_support_services(mock_db, df, mock_model)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 0


# ---------------------------------------------------------------------------
# download_dataset
# ---------------------------------------------------------------------------

class TestDownloadDataset:
    """
    download_dataset() checks whether all 5 raw files exist and calls
    save_local_copy() only when at least one is missing.

    NOTE: The original TestLoadDataset class incorrectly tested this
    download logic by patching download behaviour inside load_dataset(),
    which does NOT contain any download logic. These tests are correct.
    """

    def test_does_not_download_when_all_files_exist(self):
        """Tests that save_local_copy is NOT called when all raw files are present."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_not_called()

    def test_downloads_when_all_files_missing(self):
        """Tests that save_local_copy IS called when no raw files are present."""
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_melbourne_file_missing(self):
        """Tests that save_local_copy is called when only the Melbourne file is absent."""
        def exists_side_effect(path):
            return path != settings.MELBOURNE_RAW_PATH

        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_datagov_file_missing(self):
        """Tests that save_local_copy is called when only the DataGov file is absent."""
        def exists_side_effect(path):
            return path != settings.DATAGOV_RAW_PATH

        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_food_insecurity_file_missing(self):
        """Tests that save_local_copy is called when only the food insecurity file is absent."""
        def exists_side_effect(path):
            return path != settings.FOOD_INSECURITY_RAW_PATH

        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_vicgov_boundary_file_missing(self):
        """Tests that save_local_copy is called when only the VicGov boundary file is absent."""
        def exists_side_effect(path):
            return path != settings.VICGOV_BOUNDARY_RAW_PATH

        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_viclga_boundary_file_missing(self):
        """Tests that save_local_copy is called when only the VicLGA boundary file is absent."""
        def exists_side_effect(path):
            return path != settings.VICLGA_BOUNDARY_RAW_PATH

        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_checks_all_five_configured_paths(self):
        """Tests that os.path.exists is called for every configured raw file path."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True) as mock_exists, \
             patch("src.services.data_seeding.save_local_copy"):
            download_dataset()

        checked_paths = {c.args[0] for c in mock_exists.call_args_list}
        assert settings.MELBOURNE_RAW_PATH in checked_paths
        assert settings.DATAGOV_RAW_PATH in checked_paths
        assert settings.FOOD_INSECURITY_RAW_PATH in checked_paths
        assert settings.VICGOV_BOUNDARY_RAW_PATH in checked_paths
        assert settings.VICLGA_BOUNDARY_RAW_PATH in checked_paths

    def test_save_local_copy_called_exactly_once_when_files_missing(self):
        """Tests that save_local_copy is called exactly once — not once per missing file."""
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        assert mock_save.call_count == 1

    def test_logs_when_all_files_present(self):
        """Tests that the 'all downloaded' message is logged when no files are missing.

        Actual log message: "All data has been downloaded."
        (Original test had a wrong message: "Raw data files found. Loading from local files...")
        """
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy"), \
             patch("src.services.data_seeding.logger") as mock_logger:
            download_dataset()
        mock_logger.info.assert_any_call("All data has been downloaded.")

    def test_logs_when_files_missing(self):
        """Tests that the 'missing files' message is logged when any file is absent.

        Actual log message: "Missing files detected. Downloading..."
        (Original test had wrong message: "One or more raw data files not found. Downloading from source...")
        """
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy"), \
             patch("src.services.data_seeding.logger") as mock_logger:
            download_dataset()
        mock_logger.info.assert_any_call("Missing files detected. Downloading...")

    def test_returns_none(self):
        """Tests that download_dataset returns None (it is a void function)."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy"):
            result = download_dataset()
        assert result is None


# ---------------------------------------------------------------------------
# load_dataset
# ---------------------------------------------------------------------------

class TestLoadDataset:
    """
    load_dataset() calls the 4 loader functions and returns a 4-tuple:
        (df_emergency_services, df_food_insecurity, df_vic_boundaries, df_viclga_boundaries)

    The correct patch targets are the loader functions imported into data_seeding:
        src.services.data_seeding.load_emergency_services_dataset
        src.services.data_seeding.load_food_insecurity_dataset
        src.services.data_seeding.load_vic_boundaries_dataset
        src.services.data_seeding.load_viclga_boundaries_dataset

    NOTE: The original TestLoadDataset class:
      - patched wrangle_melbourne, wrangle_datagov, pd.read_csv — none of which
        exist in data_seeding.py (all load logic is delegated to data_loader.py)
      - assumed load_dataset() returns a single combined DataFrame — it returns a 4-tuple
      - tested download logic that lives in download_dataset(), not load_dataset()
    """

    def _patch_all_loaders(self):
        """Returns a context manager that mocks all four loader functions."""
        return (
            patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF),
            patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF),
            patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF),
            patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF),
        )

    def test_returns_four_tuple(self):
        """Tests that load_dataset returns a tuple of exactly 4 items."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            result = load_dataset()
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_first_element_is_emergency_services_dataframe(self):
        """Tests that the first tuple element is the emergency services DataFrame."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            result = load_dataset()
        df_emergency, _, _, _ = result
        assert df_emergency is EMERGENCY_DF

    def test_second_element_is_food_insecurity_dataframe(self):
        """Tests that the second tuple element is the food insecurity DataFrame."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            result = load_dataset()
        _, df_food, _, _ = result
        assert df_food is FOOD_DF

    def test_third_element_is_vic_boundaries_dataframe(self):
        """Tests that the third tuple element is the VIC boundaries DataFrame."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            result = load_dataset()
        _, _, df_vic, _ = result
        assert df_vic is VIC_DF

    def test_fourth_element_is_viclga_boundaries_dataframe(self):
        """Tests that the fourth tuple element is the VIC LGA boundaries DataFrame."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            result = load_dataset()
        _, _, _, df_lga = result
        assert df_lga is VICLGA_DF

    def test_all_four_loaders_are_called(self):
        """Tests that every loader function is invoked exactly once."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF) as mel, \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF)      as food, \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF)       as vic, \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF)    as lga:
            load_dataset()

        mel.assert_called_once()
        food.assert_called_once()
        vic.assert_called_once()
        lga.assert_called_once()

    def test_propagates_exception_from_emergency_services_loader(self):
        """Tests that a failure in load_emergency_services_dataset propagates up."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", side_effect=FileNotFoundError("missing")), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            with pytest.raises(FileNotFoundError):
                load_dataset()

    def test_propagates_exception_from_food_insecurity_loader(self):
        """Tests that a failure in load_food_insecurity_dataset propagates up."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    side_effect=FileNotFoundError("missing")), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            with pytest.raises(FileNotFoundError):
                load_dataset()

    def test_propagates_exception_from_vic_boundaries_loader(self):
        """Tests that a failure in load_vic_boundaries_dataset propagates up."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     side_effect=FileNotFoundError("missing")), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  return_value=VICLGA_DF):
            with pytest.raises(FileNotFoundError):
                load_dataset()

    def test_propagates_exception_from_viclga_boundaries_loader(self):
        """Tests that a failure in load_viclga_boundaries_dataset propagates up."""
        with patch("src.services.data_seeding.load_emergency_services_dataset", return_value=EMERGENCY_DF), \
             patch("src.services.data_seeding.load_food_insecurity_dataset",    return_value=FOOD_DF), \
             patch("src.services.data_seeding.load_vic_boundaries_dataset",     return_value=VIC_DF), \
             patch("src.services.data_seeding.load_viclga_boundaries_dataset",  side_effect=FileNotFoundError("missing")):
            with pytest.raises(FileNotFoundError):
                load_dataset()