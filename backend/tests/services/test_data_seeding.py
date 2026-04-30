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


# Sample DataFrames for each dataset type.
EMERGENCY_DF          = make_sample_df(n=2)
FOOD_DF               = pd.DataFrame({"indicator": ["food"], "estimate_pct": [10.0]})
LGA_BOUNDS_DF         = pd.DataFrame({"lga_name": ["Melbourne"], "geometry": ["POLYGON(...)"]})
LGA_POP_DF            = pd.DataFrame({"lga_name": ["Melbourne"], "lga_pid": ["LGA_PID_001"]})
DIET_INDICATOR_DF     = pd.DataFrame({"lga_name": ["Melbourne"], "diet_score": [7.5]})
HEALTH_OUTCOME_DF     = pd.DataFrame({"lga_name": ["Melbourne"], "outcome": ["diabetes"]})
LOW_COST_DIET_DF      = pd.DataFrame({"lga_name": ["Melbourne"], "weekly_cost": [120.0]})
LOW_COST_DIET_HO_DF   = pd.DataFrame({"lga_name": ["Melbourne"], "linked_outcome": ["obesity"]})


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


def _all_loader_patches(overrides: dict = None):
    """
    Returns a dict of patch kwargs for all 8 loaders with their default
    return values. Pass ``overrides`` to swap individual loaders
    (e.g. ``{"load_emergency_services_dataset": side_effect=...}``).
    """
    defaults = {
        "load_emergency_services_dataset":          EMERGENCY_DF,
        "load_food_insecurity_dataset":             FOOD_DF,
        "load_lga_boundaries_dataset":              LGA_BOUNDS_DF,
        "load_lga_population_dataset":              LGA_POP_DF,
        "load_diet_indicator_dataset":              DIET_INDICATOR_DF,
        "load_health_outcome_dataset":              HEALTH_OUTCOME_DF,
        "load_low_cost_diet_dataset":               LOW_COST_DIET_DF,
        "load_low_cost_diet_health_outcome_dataset": LOW_COST_DIET_HO_DF,
    }
    if overrides:
        defaults.update(overrides)
    return defaults


# ---------------------------------------------------------------------------
# seed_support_services
# ---------------------------------------------------------------------------

class TestSeedSupportServices:
    """seed_support_services(db, df, model) requires THREE arguments."""

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
        seed_support_services(mock_db, make_sample_df(), mock_model)
        assert call_order == ["delete", "bulk_save"]

    def test_bulk_saves_correct_number_of_objects(self, mock_db, mock_model):
        """Tests that the correct number of model instances are bulk-saved."""
        seed_support_services(mock_db, make_sample_df(n=3), mock_model)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 3

    def test_model_instantiated_from_each_row(self, mock_db, mock_model):
        """Tests that the model constructor is called once per DataFrame row."""
        seed_support_services(mock_db, make_sample_df(n=4), mock_model)
        assert mock_model.call_count == 4

    def test_commits_after_successful_insert(self, mock_db, mock_model):
        """Tests that db.commit() is called after a successful bulk save."""
        seed_support_services(mock_db, make_sample_df(), mock_model)
        mock_db.commit.assert_called_once()

    def test_rollback_on_bulk_save_exception(self, mock_db, mock_model):
        """Tests that db.rollback() is called when bulk_save_objects raises."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            seed_support_services(mock_db, make_sample_df(), mock_model)
        mock_db.rollback.assert_called_once()

    def test_rollback_on_delete_exception(self, mock_db, mock_model):
        """Tests that db.rollback() is called when the initial delete raises."""
        mock_db.query.return_value.delete.side_effect = Exception("Delete failed")
        with pytest.raises(Exception):
            seed_support_services(mock_db, make_sample_df(), mock_model)
        mock_db.rollback.assert_called_once()

    def test_reraises_exception_after_rollback(self, mock_db, mock_model):
        """Tests that the original exception is re-raised after rollback."""
        mock_db.bulk_save_objects.side_effect = RuntimeError("Unexpected failure")
        with pytest.raises(RuntimeError, match="Unexpected failure"):
            seed_support_services(mock_db, make_sample_df(), mock_model)

    def test_does_not_commit_on_exception(self, mock_db, mock_model):
        """Tests that db.commit() is NOT called when an exception occurs."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            seed_support_services(mock_db, make_sample_df(), mock_model)
        mock_db.commit.assert_not_called()

    def test_returns_none(self, mock_db, mock_model):
        """Tests that seed_support_services returns None."""
        result = seed_support_services(mock_db, make_sample_df(), mock_model)
        assert result is None

    def test_logs_start_with_record_count(self, mock_db, mock_model):
        """Tests that the start log includes the number of records to be inserted."""
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, make_sample_df(n=5), mock_model)
        mock_logger.info.assert_any_call("Starting database seed with 5 records...")

    def test_logs_success_with_inserted_count(self, mock_db, mock_model):
        """Tests that a success log is emitted with the count of inserted records."""
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, make_sample_df(n=2), mock_model)
        mock_logger.info.assert_any_call(
            "Database seeding completed successfully! Inserted 2 records."
        )

    def test_logs_error_on_exception(self, mock_db, mock_model):
        """Tests that an error is logged when an exception occurs."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        with patch("src.services.data_seeding.logger") as mock_logger:
            with pytest.raises(Exception):
                seed_support_services(mock_db, make_sample_df(), mock_model)
        mock_logger.error.assert_called_once()

    def test_empty_dataframe_still_deletes_and_commits(self, mock_db, mock_model):
        """Tests that an empty DataFrame still triggers delete and commit."""
        seed_support_services(mock_db, make_sample_df(n=0), mock_model)
        mock_db.query.return_value.delete.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_empty_dataframe_bulk_saves_zero_objects(self, mock_db, mock_model):
        """Tests that an empty DataFrame passes an empty list to bulk_save_objects."""
        seed_support_services(mock_db, make_sample_df(n=0), mock_model)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 0


# ---------------------------------------------------------------------------
# download_dataset
# ---------------------------------------------------------------------------

class TestDownloadDataset:
    """
    download_dataset() checks whether all 6 raw files exist:
        MELBOURNE_RAW_PATH, DATAGOV_RAW_PATH, FOOD_INSECURITY_RAW_PATH,
        VICLGA_BOUNDARY_RAW_PATH, LGA_POPULATION_RAW_PATH, DIET_INDICATOR_RAW_PATH
    and calls save_local_copy() only when at least one is missing.
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
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.MELBOURNE_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_datagov_file_missing(self):
        """Tests that save_local_copy is called when only the DataGov file is absent."""
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.DATAGOV_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_food_insecurity_file_missing(self):
        """Tests that save_local_copy is called when only the food insecurity file is absent."""
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.FOOD_INSECURITY_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_viclga_boundary_file_missing(self):
        """Tests that save_local_copy is called when only the VicLGA boundary file is absent."""
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.VICLGA_BOUNDARY_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_lga_population_file_missing(self):
        """Tests that save_local_copy is called when only the LGA population file is absent."""
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.LGA_POPULATION_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_downloads_when_only_diet_indicator_file_missing(self):
        """Tests that save_local_copy is called when only the diet indicator file is absent."""
        with patch("src.services.data_seeding.os.path.exists",
                   side_effect=lambda p: p != settings.DIET_INDICATOR_RAW_PATH), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        mock_save.assert_called_once()

    def test_checks_all_six_configured_paths(self):
        """Tests that os.path.exists is called for every configured raw file path."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True) as mock_exists, \
             patch("src.services.data_seeding.save_local_copy"):
            download_dataset()
        checked = {c.args[0] for c in mock_exists.call_args_list}
        assert settings.MELBOURNE_RAW_PATH        in checked
        assert settings.DATAGOV_RAW_PATH          in checked
        assert settings.FOOD_INSECURITY_RAW_PATH  in checked
        assert settings.VICLGA_BOUNDARY_RAW_PATH  in checked
        assert settings.LGA_POPULATION_RAW_PATH   in checked
        assert settings.DIET_INDICATOR_RAW_PATH   in checked

    def test_save_local_copy_called_exactly_once_when_files_missing(self):
        """Tests that save_local_copy is called exactly once — not once per missing file."""
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy") as mock_save:
            download_dataset()
        assert mock_save.call_count == 1

    def test_logs_when_all_files_present(self):
        """Tests that 'All data has been downloaded.' is logged when no files are missing."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy"), \
             patch("src.services.data_seeding.logger") as mock_logger:
            download_dataset()
        mock_logger.info.assert_any_call("All data has been downloaded.")

    def test_logs_when_files_missing(self):
        """Tests that 'Missing files detected. Downloading...' is logged when any file is absent."""
        with patch("src.services.data_seeding.os.path.exists", return_value=False), \
             patch("src.services.data_seeding.save_local_copy"), \
             patch("src.services.data_seeding.logger") as mock_logger:
            download_dataset()
        mock_logger.info.assert_any_call("Missing files detected. Downloading...")

    def test_returns_none(self):
        """Tests that download_dataset returns None."""
        with patch("src.services.data_seeding.os.path.exists", return_value=True), \
             patch("src.services.data_seeding.save_local_copy"):
            result = download_dataset()
        assert result is None


# ---------------------------------------------------------------------------
# load_dataset
# ---------------------------------------------------------------------------

class TestLoadDataset:
    """
    load_dataset() calls 8 loaders and returns a list of 8 (df, model) tuples
    in the following order:
        (emergency_services_df, SupportService),
        (food_insecurity_df,    FoodInsecurity),
        (lga_boundaries_df,     VicLgaBoundary),
        (lga_population_df,     LgaPopulation),
        (diet_indicator_df,     DietIndicator),
        (health_outcome_df,     HealthOutcome),
        (low_cost_diet_df,      LowCostDiet),
        (low_cost_diet_ho_df,   LowCostDietHealthOutcome),

    Correct patch targets (functions imported into data_seeding):
        src.services.data_seeding.load_emergency_services_dataset
        src.services.data_seeding.load_food_insecurity_dataset
        src.services.data_seeding.load_lga_boundaries_dataset
        src.services.data_seeding.load_lga_population_dataset
        src.services.data_seeding.load_diet_indicator_dataset
        src.services.data_seeding.load_health_outcome_dataset
        src.services.data_seeding.load_low_cost_diet_dataset
        src.services.data_seeding.load_low_cost_diet_health_outcome_dataset
    """

    BASE = "src.services.data_seeding"

    def _patch_all(self, overrides: dict = None):
        """
        Context manager that patches all 8 loaders. ``overrides`` maps a
        short loader name to a ``side_effect`` or ``return_value`` dict,
        e.g. ``{"load_emergency_services_dataset": {"side_effect": FileNotFoundError()}}``.
        """
        patches_cfg = _all_loader_patches()
        active_patches = []
        mocks = {}
        for name, df in patches_cfg.items():
            target = f"{self.BASE}.{name}"
            kw = {"return_value": df}
            if overrides and name in overrides:
                kw = overrides[name]
            p = patch(target, **kw)
            active_patches.append(p)
            mocks[name] = p
        return active_patches

    # -- helpers --

    def _run_with_all_patches(self, overrides=None):
        patches_cfg = _all_loader_patches()
        ctx = {}
        patch_objs = []
        for name, df in patches_cfg.items():
            target = f"{self.BASE}.{name}"
            if overrides and name in overrides:
                p = patch(target, **overrides[name])
            else:
                p = patch(target, return_value=df)
            patch_objs.append(p)

        started = [p.start() for p in patch_objs]
        try:
            result = load_dataset()
        finally:
            for p in patch_objs:
                p.stop()
        return result, started

    # -- structure tests --

    def test_returns_list(self):
        """Tests that load_dataset returns a list."""
        result, _ = self._run_with_all_patches()
        assert isinstance(result, list)

    def test_returns_eight_items(self):
        """Tests that load_dataset returns exactly 8 (df, model) pairs."""
        result, _ = self._run_with_all_patches()
        assert len(result) == 8

    def test_each_item_is_two_tuple(self):
        """Tests that every item in the result is a 2-tuple of (DataFrame, model class)."""
        result, _ = self._run_with_all_patches()
        for item in result:
            assert len(item) == 2

    def test_each_first_element_is_dataframe(self):
        """Tests that the first element of every pair is a DataFrame."""
        result, _ = self._run_with_all_patches()
        for df, _ in result:
            assert isinstance(df, pd.DataFrame)

    # -- ordering / identity tests --

    def test_first_pair_is_emergency_services(self):
        """Tests that the first pair contains the emergency services DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[0]
        assert df is EMERGENCY_DF

    def test_second_pair_is_food_insecurity(self):
        """Tests that the second pair contains the food insecurity DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[1]
        assert df is FOOD_DF

    def test_third_pair_is_lga_boundaries(self):
        """Tests that the third pair contains the LGA boundaries DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[2]
        assert df is LGA_BOUNDS_DF

    def test_fourth_pair_is_lga_population(self):
        """Tests that the fourth pair contains the LGA population DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[3]
        assert df is LGA_POP_DF

    def test_fifth_pair_is_diet_indicator(self):
        """Tests that the fifth pair contains the diet indicator DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[4]
        assert df is DIET_INDICATOR_DF

    def test_sixth_pair_is_health_outcome(self):
        """Tests that the sixth pair contains the health outcome DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[5]
        assert df is HEALTH_OUTCOME_DF

    def test_seventh_pair_is_low_cost_diet(self):
        """Tests that the seventh pair contains the low cost diet DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[6]
        assert df is LOW_COST_DIET_DF

    def test_eighth_pair_is_low_cost_diet_health_outcome(self):
        """Tests that the eighth pair contains the low cost diet health outcome DataFrame."""
        result, _ = self._run_with_all_patches()
        df, _ = result[7]
        assert df is LOW_COST_DIET_HO_DF

    # -- all loaders called --

    def test_all_eight_loaders_are_called(self):
        """Tests that every loader function is invoked exactly once."""
        loader_names = list(_all_loader_patches().keys())
        patch_objs = []
        mocks = []
        for name in loader_names:
            df = _all_loader_patches()[name]
            p = patch(f"{self.BASE}.{name}", return_value=df)
            patch_objs.append(p)
            mocks.append(p.start())
        try:
            load_dataset()
        finally:
            for p in patch_objs:
                p.stop()
        for m in mocks:
            m.assert_called_once()

    # -- exception propagation --

    def _assert_propagates(self, failing_loader: str):
        overrides = {failing_loader: {"side_effect": FileNotFoundError("missing")}}
        with pytest.raises(FileNotFoundError):
            self._run_with_all_patches(overrides=overrides)

    def test_propagates_exception_from_emergency_services_loader(self):
        """Tests that a failure in load_emergency_services_dataset propagates up."""
        self._assert_propagates("load_emergency_services_dataset")

    def test_propagates_exception_from_food_insecurity_loader(self):
        """Tests that a failure in load_food_insecurity_dataset propagates up."""
        self._assert_propagates("load_food_insecurity_dataset")

    def test_propagates_exception_from_lga_boundaries_loader(self):
        """Tests that a failure in load_lga_boundaries_dataset propagates up."""
        self._assert_propagates("load_lga_boundaries_dataset")

    def test_propagates_exception_from_lga_population_loader(self):
        """Tests that a failure in load_lga_population_dataset propagates up."""
        self._assert_propagates("load_lga_population_dataset")

    def test_propagates_exception_from_diet_indicator_loader(self):
        """Tests that a failure in load_diet_indicator_dataset propagates up."""
        self._assert_propagates("load_diet_indicator_dataset")

    def test_propagates_exception_from_health_outcome_loader(self):
        """Tests that a failure in load_health_outcome_dataset propagates up."""
        self._assert_propagates("load_health_outcome_dataset")

    def test_propagates_exception_from_low_cost_diet_loader(self):
        """Tests that a failure in load_low_cost_diet_dataset propagates up."""
        self._assert_propagates("load_low_cost_diet_dataset")

    def test_propagates_exception_from_low_cost_diet_health_outcome_loader(self):
        """Tests that a failure in load_low_cost_diet_health_outcome_dataset propagates up."""
        self._assert_propagates("load_low_cost_diet_health_outcome_dataset")