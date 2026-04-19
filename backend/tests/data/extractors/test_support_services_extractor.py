import io
import zipfile
import pytest
import pandas as pd
import geopandas as gpd
import requests
from unittest.mock import patch, MagicMock, call

from src.data.extractors.support_services_extractor import (
    _download_content,
    fetch_csv_from_url,
    fetch_excel_from_url,
    fetch_gdb_from_url,
    fetch_zip_from_url,
)


# ---------------------------------------------------------------------------
# Shared helpers / fixtures
# ---------------------------------------------------------------------------

SAMPLE_CSV_COMMA = "name,age,city\nAlice,30,Melbourne\nBob,25,Sydney"
SAMPLE_CSV_SEMICOLON = "name;age;city\nAlice;30;Melbourne\nBob;25;Sydney"
TEST_URL = "https://example.com/data"


def make_mock_response(content, status_code: int = 200, as_bytes: bool = False):
    """Creates a mock requests.Response for testing.

    Args:
        content: Response body — str for text responses, bytes for binary.
        status_code: HTTP status code to simulate.
        as_bytes: When True, `.content` returns the raw bytes; `.text` is unused.
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    if as_bytes:
        mock_response.content = content
    else:
        mock_response.text = content
        mock_response.content = content.encode() if isinstance(content, str) else content
    mock_response.raise_for_status = MagicMock()
    if status_code >= 400:
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
    return mock_response


def make_excel_bytes(sheet_name="Sheet1") -> bytes:
    """Creates a minimal in-memory Excel file and returns its raw bytes."""
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return buf.getvalue()


def make_zip_bytes(inner_filename: str = "test.txt", inner_content: bytes = b"hello") -> bytes:
    """Creates a minimal in-memory ZIP archive and returns its raw bytes."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(inner_filename, inner_content)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# _download_content
# ---------------------------------------------------------------------------

class TestDownloadContent:
    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_returns_text_by_default(self, mock_get):
        """Tests that as_bytes=False returns response.text."""
        mock_get.return_value = make_mock_response("hello text")
        result = _download_content(TEST_URL, as_bytes=False)
        assert result == "hello text"

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_returns_bytes_when_requested(self, mock_get):
        """Tests that as_bytes=True returns response.content."""
        raw = b"\x89PNG\r\n"
        mock_get.return_value = make_mock_response(raw, as_bytes=True)
        result = _download_content(TEST_URL, as_bytes=True)
        assert result == raw

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_passes_timeout_to_requests(self, mock_get):
        """Tests that requests.get is called with a timeout for safety."""
        mock_get.return_value = make_mock_response("ok")
        _download_content(TEST_URL, as_bytes=False)
        _, kwargs = mock_get.call_args
        assert "timeout" in kwargs, "requests.get should be called with a timeout"

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_calls_correct_url(self, mock_get):
        """Tests that requests.get is called with the correct URL."""
        mock_get.return_value = make_mock_response("ok")
        _download_content(TEST_URL, as_bytes=False)
        args, _ = mock_get.call_args
        assert args[0] == TEST_URL

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_http_404(self, mock_get):
        """Tests that an HTTPError is raised for 404 responses."""
        mock_get.return_value = make_mock_response("Not Found", status_code=404)
        with pytest.raises(requests.exceptions.HTTPError):
            _download_content(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_http_500(self, mock_get):
        """Tests that an HTTPError is raised for 500 responses."""
        mock_get.return_value = make_mock_response("Server Error", status_code=500)
        with pytest.raises(requests.exceptions.HTTPError):
            _download_content(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_connection_error(self, mock_get):
        """Tests that a ConnectionError propagates correctly."""
        mock_get.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(requests.exceptions.ConnectionError):
            _download_content(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_timeout(self, mock_get):
        """Tests that a Timeout error propagates correctly."""
        mock_get.side_effect = requests.exceptions.Timeout
        with pytest.raises(requests.exceptions.Timeout):
            _download_content(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_logs_fetch_info(self, mock_get):
        """Tests that fetching is logged at INFO level with the correct URL."""
        mock_get.return_value = make_mock_response("ok")
        with patch("src.data.extractors.support_services_extractor.logger") as mock_logger:
            _download_content(TEST_URL, as_bytes=False)
            mock_logger.info.assert_called_once_with(f"Fetching data from {TEST_URL}")


# ---------------------------------------------------------------------------
# fetch_csv_from_url
# ---------------------------------------------------------------------------

class TestFetchCsvFromUrl:
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_returns_dataframe(self, mock_download):
        """Tests that the function returns a DataFrame."""
        mock_download.return_value = SAMPLE_CSV_COMMA
        result = fetch_csv_from_url(TEST_URL)
        assert isinstance(result, pd.DataFrame)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_default_separator_is_comma(self, mock_download):
        """Tests that the default separator correctly parses comma-delimited CSV."""
        mock_download.return_value = SAMPLE_CSV_COMMA
        result = fetch_csv_from_url(TEST_URL)
        assert list(result.columns) == ["name", "age", "city"]
        assert len(result) == 2

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_custom_separator_semicolon(self, mock_download):
        """Tests that a semicolon separator parses the CSV correctly."""
        mock_download.return_value = SAMPLE_CSV_SEMICOLON
        result = fetch_csv_from_url(TEST_URL, separator=";")
        assert list(result.columns) == ["name", "age", "city"]
        assert len(result) == 2

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_dataframe_values_are_correct(self, mock_download):
        """Tests that parsed DataFrame values match the source CSV."""
        mock_download.return_value = SAMPLE_CSV_COMMA
        result = fetch_csv_from_url(TEST_URL)
        assert result.iloc[0]["name"] == "Alice"
        assert result.iloc[1]["name"] == "Bob"
        assert result.iloc[0]["city"] == "Melbourne"

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_calls_download_content_with_correct_args(self, mock_download):
        """Tests that _download_content is called with as_bytes=False for CSV."""
        mock_download.return_value = SAMPLE_CSV_COMMA
        fetch_csv_from_url(TEST_URL)
        mock_download.assert_called_once_with(TEST_URL, as_bytes=False)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_empty_csv_returns_empty_dataframe(self, mock_download):
        """Tests that a header-only CSV returns an empty DataFrame with correct columns."""
        mock_download.return_value = "name,age,city\n"
        result = fetch_csv_from_url(TEST_URL)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert list(result.columns) == ["name", "age", "city"]

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_wrong_separator_produces_single_column(self, mock_download):
        """Tests that using the wrong separator results in unparsed single-column output."""
        mock_download.return_value = SAMPLE_CSV_SEMICOLON
        result = fetch_csv_from_url(TEST_URL, separator=",")  # wrong sep
        assert len(result.columns) == 1  # whole line becomes one column

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_http_error_from_download(self, mock_download):
        """Tests that HTTPErrors from _download_content propagate to the caller."""
        mock_download.side_effect = requests.exceptions.HTTPError
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_csv_from_url(TEST_URL)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_connection_error_from_download(self, mock_download):
        """Tests that ConnectionErrors from _download_content propagate to the caller."""
        mock_download.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_csv_from_url(TEST_URL)


# ---------------------------------------------------------------------------
# fetch_excel_from_url
# ---------------------------------------------------------------------------

class TestFetchExcelFromUrl:
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_returns_dataframe(self, mock_download):
        """Tests that the function returns a DataFrame."""
        mock_download.return_value = make_excel_bytes()
        result = fetch_excel_from_url(TEST_URL)
        assert isinstance(result, pd.DataFrame)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_default_sheet_name_is_zero(self, mock_download):
        """Tests that the default sheet index is 0 (first sheet)."""
        mock_download.return_value = make_excel_bytes()
        result = fetch_excel_from_url(TEST_URL)
        assert list(result.columns) == ["col1", "col2"]
        assert len(result) == 2

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_custom_sheet_name(self, mock_download):
        """Tests that a named sheet can be read correctly."""
        mock_download.return_value = make_excel_bytes(sheet_name="MySheet")
        result = fetch_excel_from_url(TEST_URL, sheet_name="MySheet")
        assert list(result.columns) == ["col1", "col2"]

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_calls_download_content_with_as_bytes_true(self, mock_download):
        """Tests that _download_content is called with as_bytes=True for binary Excel."""
        mock_download.return_value = make_excel_bytes()
        fetch_excel_from_url(TEST_URL)
        mock_download.assert_called_once_with(TEST_URL)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_dataframe_values_are_correct(self, mock_download):
        """Tests that parsed DataFrame values match the source Excel content."""
        mock_download.return_value = make_excel_bytes()
        result = fetch_excel_from_url(TEST_URL)
        assert result.iloc[0]["col1"] == 1
        assert result.iloc[1]["col2"] == "b"

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_http_error_from_download(self, mock_download):
        """Tests that HTTPErrors from _download_content propagate to the caller."""
        mock_download.side_effect = requests.exceptions.HTTPError
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_excel_from_url(TEST_URL)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_raises_on_invalid_sheet_name(self, mock_download):
        """Tests that requesting a non-existent sheet raises an error."""
        mock_download.return_value = make_excel_bytes(sheet_name="RealSheet")
        with pytest.raises(Exception):  # xlrd.XLRDError or ValueError depending on engine
            fetch_excel_from_url(TEST_URL, sheet_name="NonExistentSheet")


# ---------------------------------------------------------------------------
# fetch_gdb_from_url
# ---------------------------------------------------------------------------

class TestFetchGdbFromUrl:
    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_returns_geodataframe(self, mock_download, mock_read_file):
        """Tests that the function returns a GeoDataFrame."""
        mock_download.return_value = b"fake-gdb-bytes"
        mock_read_file.return_value = gpd.GeoDataFrame({"geometry": []})
        result = fetch_gdb_from_url(TEST_URL)
        assert isinstance(result, gpd.GeoDataFrame)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_calls_download_content_with_as_bytes_true(self, mock_download, mock_read_file):
        """Tests that _download_content is called with default as_bytes=True."""
        mock_download.return_value = b"fake-gdb-bytes"
        mock_read_file.return_value = gpd.GeoDataFrame()
        fetch_gdb_from_url(TEST_URL)
        mock_download.assert_called_once_with(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_passes_bytes_buffer_to_read_file(self, mock_download, mock_read_file):
        """Tests that gpd.read_file receives a BytesIO object, not raw bytes."""
        mock_download.return_value = b"fake-gdb-bytes"
        mock_read_file.return_value = gpd.GeoDataFrame()
        fetch_gdb_from_url(TEST_URL)
        args, _ = mock_read_file.call_args
        assert isinstance(args[0], io.BytesIO)

    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_http_error_from_download(self, mock_download):
        """Tests that HTTPErrors from _download_content propagate to the caller."""
        mock_download.side_effect = requests.exceptions.HTTPError
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_gdb_from_url(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_read_file_error(self, mock_download, mock_read_file):
        """Tests that errors from gpd.read_file propagate to the caller."""
        mock_download.return_value = b"invalid-bytes"
        mock_read_file.side_effect = Exception("Cannot read GDB")
        with pytest.raises(Exception, match="Cannot read GDB"):
            fetch_gdb_from_url(TEST_URL)


# ---------------------------------------------------------------------------
# fetch_zip_from_url
# ---------------------------------------------------------------------------

class TestFetchZipFromUrl:
    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_returns_geodataframe(self, mock_download, mock_settings, mock_read_file):
        """Tests that the function returns a GeoDataFrame."""
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = "/tmp/test_unzip"
        mock_download.return_value = make_zip_bytes()
        mock_read_file.return_value = gpd.GeoDataFrame({"geometry": []})
        result = fetch_zip_from_url(TEST_URL)
        assert isinstance(result, gpd.GeoDataFrame)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_calls_download_content_with_as_bytes_true(
        self, mock_download, mock_settings, mock_read_file
    ):
        """Tests that _download_content is called with as_bytes=True (default)."""
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = "/tmp/test_unzip"
        mock_download.return_value = make_zip_bytes()
        mock_read_file.return_value = gpd.GeoDataFrame()
        fetch_zip_from_url(TEST_URL)
        mock_download.assert_called_once_with(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_extracts_to_correct_directory(
        self, mock_download, mock_settings, mock_read_file
    ):
        """Tests that the ZIP is extracted to the path defined in settings."""
        unzip_path = "/tmp/test_unzip_dir"
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = unzip_path
        mock_download.return_value = make_zip_bytes()
        mock_read_file.return_value = gpd.GeoDataFrame()

        with patch("src.data.extractors.support_services_extractor.zipfile.ZipFile") as mock_zip_cls:
            mock_zip = MagicMock()
            mock_zip_cls.return_value.__enter__ = MagicMock(return_value=mock_zip)
            mock_zip_cls.return_value.__exit__ = MagicMock(return_value=False)
            fetch_zip_from_url(TEST_URL)
            mock_zip.extractall.assert_called_once_with(unzip_path)

    @patch("src.data.extractors.support_services_extractor.gpd.read_file")
    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_reads_shapefile_from_correct_path(
        self, mock_download, mock_settings, mock_read_file
    ):
        """Tests that gpd.read_file is called with the expected .shp path."""
        unzip_path = "/tmp/test_unzip_dir"
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = unzip_path
        mock_download.return_value = make_zip_bytes()
        mock_read_file.return_value = gpd.GeoDataFrame()

        with patch("src.data.extractors.support_services_extractor.zipfile.ZipFile") as mock_zip_cls:
            mock_zip_cls.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_zip_cls.return_value.__exit__ = MagicMock(return_value=False)
            fetch_zip_from_url(TEST_URL)

        expected_shp_path = f"{unzip_path}/VIC_LGA_GDA2020/vic_lga.shp"
        mock_read_file.assert_called_once_with(expected_shp_path)

    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_propagates_http_error_from_download(self, mock_download, mock_settings):
        """Tests that HTTPErrors from _download_content propagate to the caller."""
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = "/tmp/test_unzip"
        mock_download.side_effect = requests.exceptions.HTTPError
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_zip_from_url(TEST_URL)

    @patch("src.data.extractors.support_services_extractor.settings")
    @patch("src.data.extractors.support_services_extractor._download_content")
    def test_raises_on_invalid_zip_content(self, mock_download, mock_settings):
        """Tests that invalid (non-ZIP) byte content raises a BadZipFile error."""
        mock_settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH = "/tmp/test_unzip"
        mock_download.return_value = b"this is not a zip file"
        with pytest.raises(zipfile.BadZipFile):
            fetch_zip_from_url(TEST_URL)