import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, call

from src.services.data_seeding import seed_support_services, load_dataset


# ---------------------------------------------------------------------------
# Shared helpers & fixtures
# ---------------------------------------------------------------------------

def make_sample_df(n=2):
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


@pytest.fixture
def mock_db():
    """A mock SQLAlchemy Session with all required methods."""
    db = MagicMock()
    db.query.return_value.delete.return_value = None
    db.bulk_save_objects.return_value = None
    db.commit.return_value = None
    db.rollback.return_value = None
    return db


# ---------------------------------------------------------------------------
# seed_support_services
# ---------------------------------------------------------------------------

class TestSeedSupportServices:
    def test_deletes_existing_records_before_insert(self, mock_db):
        """Tests that existing records are deleted before insertion."""
        from src.models import SupportService
        df = make_sample_df()
        seed_support_services(mock_db, df)
        mock_db.query.assert_called_once_with(SupportService)
        mock_db.query.return_value.delete.assert_called_once()

    def test_bulk_saves_correct_number_of_objects(self, mock_db):
        """Tests that the correct number of objects are bulk saved."""
        df = make_sample_df(n=3)
        seed_support_services(mock_db, df)
        args, _ = mock_db.bulk_save_objects.call_args
        assert len(args[0]) == 3

    def test_commits_after_insert(self, mock_db):
        """Tests that the database is committed after insertion."""
        df = make_sample_df()
        seed_support_services(mock_db, df)
        mock_db.commit.assert_called_once()

    def test_rollback_on_exception(self, mock_db):
        """Tests that the database is rolled back on exception."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with pytest.raises(Exception, match="DB error"):
            seed_support_services(mock_db, df)
        mock_db.rollback.assert_called_once()

    def test_re_raises_exception_after_rollback(self, mock_db):
        """Tests that the exception is re-raised after rollback."""
        mock_db.bulk_save_objects.side_effect = RuntimeError("Unexpected failure")
        df = make_sample_df()
        with pytest.raises(RuntimeError, match="Unexpected failure"):
            seed_support_services(mock_db, df)

    def test_does_not_commit_on_exception(self, mock_db):
        """Tests that the database is not committed on exception."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with pytest.raises(Exception):
            seed_support_services(mock_db, df)
        mock_db.commit.assert_not_called()

    def test_returns_none(self, mock_db):
        """Tests that the function returns None."""
        df = make_sample_df()
        result = seed_support_services(mock_db, df)
        assert result is None

    def test_logs_start_with_record_count(self, mock_db):
        """Tests that the function logs the start with the record count."""
        df = make_sample_df(n=5)
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, df)
        mock_logger.info.assert_any_call("Starting database seed with 5 records...")

    def test_logs_success_with_inserted_count(self, mock_db):
        """Tests that the function logs the success with the inserted count."""
        df = make_sample_df(n=2)
        with patch("src.services.data_seeding.logger") as mock_logger:
            seed_support_services(mock_db, df)
        mock_logger.info.assert_any_call(
            "Database seeding completed successfully! Inserted 2 records."
        )

    def test_logs_error_on_exception(self, mock_db):
        """Tests that the function logs the error on exception."""
        mock_db.bulk_save_objects.side_effect = Exception("DB error")
        df = make_sample_df()
        with patch("src.services.data_seeding.logger") as mock_logger:
            with pytest.raises(Exception):
                seed_support_services(mock_db, df)
        mock_logger.error.assert_called_once()

    def test_empty_dataframe_still_deletes_and_commits(self, mock_db):
        """Tests that an empty dataframe still deletes and commits."""
        df = make_sample_df(n=0)
        seed_support_services(mock_db, df)
        mock_db.query.return_value.delete.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_delete_is_called_before_bulk_save(self, mock_db):
        """Verifies delete precedes insert to prevent duplicates."""
        call_order = []
        mock_db.query.return_value.delete.side_effect = lambda: call_order.append("delete")
        mock_db.bulk_save_objects.side_effect = lambda objs: call_order.append("bulk_save")
        df = make_sample_df()
        seed_support_services(mock_db, df)
        assert call_order == ["delete", "bulk_save"]


# ---------------------------------------------------------------------------
# load_dataset
# ---------------------------------------------------------------------------

class TestLoadDataset:
    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_does_not_download_when_both_files_exist(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function does not download when both files exist."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        load_dataset()
        mock_save.assert_not_called()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=False)
    def test_downloads_when_both_files_missing(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function downloads when both files are missing."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        load_dataset()
        mock_save.assert_called_once()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    def test_downloads_when_only_melbourne_file_missing(
        self, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function downloads when only the Melbourne file is missing."""
        from src.core.config import settings
        def exists_side_effect(path):
            return path != settings.MELBOURNE_RAW_PATH
        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect):
            mock_read_csv.return_value = make_sample_df()
            mock_wrangle_mel.return_value = make_sample_df()
            mock_wrangle_dg.return_value = make_sample_df()
            load_dataset()
        mock_save.assert_called_once()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    def test_downloads_when_only_datagov_file_missing(
        self, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function downloads when only the DataGov file is missing."""
        from src.core.config import settings
        def exists_side_effect(path):
            return path != settings.DATAGOV_RAW_PATH
        with patch("src.services.data_seeding.os.path.exists", side_effect=exists_side_effect):
            mock_read_csv.return_value = make_sample_df()
            mock_wrangle_mel.return_value = make_sample_df()
            mock_wrangle_dg.return_value = make_sample_df()
            load_dataset()
        mock_save.assert_called_once()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_reads_csv_from_correct_paths(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function reads CSV from the correct paths."""
        from src.core.config import settings
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        load_dataset()
        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.MELBOURNE_RAW_PATH in paths_called
        assert settings.DATAGOV_RAW_PATH in paths_called

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_applies_wrangling_pipelines(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function applies the wrangling pipelines."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        load_dataset()
        mock_wrangle_mel.assert_called_once()
        mock_wrangle_dg.assert_called_once()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_returns_combined_dataframe(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function returns a combined dataframe."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df(n=2)
        mock_wrangle_dg.return_value = make_sample_df(n=3)
        result = load_dataset()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_result_is_sorted_by_name(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the result is sorted by name."""
        mel_df = pd.DataFrame([{"name": "Zoo Service"}, {"name": "Alpha Service"}])
        dg_df = pd.DataFrame([{"name": "Middle Service"}])
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = mel_df
        mock_wrangle_dg.return_value = dg_df
        result = load_dataset()
        names = list(result["name"])
        assert names == sorted(names)

    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_raises_when_melbourne_csv_unreadable(
        self, mock_exists, mock_save, mock_read_csv
    ):
        """Tests that the function raises an error when the Melbourne CSV is unreadable."""
        from src.core.config import settings
        def read_csv_side_effect(path):
            if path == settings.MELBOURNE_RAW_PATH:
                raise FileNotFoundError("File not found")
            return make_sample_df()
        mock_read_csv.side_effect = read_csv_side_effect
        with pytest.raises(FileNotFoundError):
            load_dataset()

    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_raises_when_datagov_csv_unreadable(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel
    ):
        """Tests that the function raises an error when the DataGov CSV is unreadable."""
        from src.core.config import settings
        mock_wrangle_mel.return_value = make_sample_df()
        def read_csv_side_effect(path):
            if path == settings.DATAGOV_RAW_PATH:
                raise FileNotFoundError("File not found")
            return make_sample_df()
        mock_read_csv.side_effect = read_csv_side_effect
        with pytest.raises(FileNotFoundError):
            load_dataset()

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=True)
    def test_logs_when_files_found_locally(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function logs when files are found locally."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        with patch("src.services.data_seeding.logger") as mock_logger:
            load_dataset()
        mock_logger.info.assert_any_call("Raw data files found. Loading from local files...")

    @patch("src.services.data_seeding.wrangle_datagov")
    @patch("src.services.data_seeding.wrangle_melbourne")
    @patch("src.services.data_seeding.pd.read_csv")
    @patch("src.services.data_seeding.save_local_copy")
    @patch("src.services.data_seeding.os.path.exists", return_value=False)
    def test_logs_when_files_missing(
        self, mock_exists, mock_save, mock_read_csv, mock_wrangle_mel, mock_wrangle_dg
    ):
        """Tests that the function logs when files are missing."""
        mock_read_csv.return_value = make_sample_df()
        mock_wrangle_mel.return_value = make_sample_df()
        mock_wrangle_dg.return_value = make_sample_df()
        with patch("src.services.data_seeding.logger") as mock_logger:
            load_dataset()
        mock_logger.info.assert_any_call(
            "One or more raw data files not found. Downloading from source..."
        )