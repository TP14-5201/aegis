
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from src.data.extractors.support_services_extractor import fetch_csv_from_url


SAMPLE_CSV_COMMA = "name,age,city\nAlice,30,Melbourne\nBob,25,Sydney"
SAMPLE_CSV_SEMICOLON = "name;age;city\nAlice;30;Melbourne\nBob;25;Sydney"


def make_mock_response(text: str, status_code: int = 200):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.text = text
    mock_response.raise_for_status = MagicMock()
    if status_code >= 400:
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
    return mock_response


class TestFetchCsvFromUrl:
    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_returns_dataframe(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_COMMA)
        result = fetch_csv_from_url("https://example.com/data.csv")
        assert isinstance(result, pd.DataFrame)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_default_separator_is_comma(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_COMMA)
        result = fetch_csv_from_url("https://example.com/data.csv")
        assert list(result.columns) == ["name", "age", "city"]
        assert len(result) == 2

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_custom_separator_semicolon(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_SEMICOLON)
        result = fetch_csv_from_url("https://example.com/data.csv", separator=";")
        assert list(result.columns) == ["name", "age", "city"]
        assert len(result) == 2

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_correct_url_is_called(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_COMMA)
        url = "https://example.com/data.csv"
        fetch_csv_from_url(url)
        mock_get.assert_called_once_with(url)

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_dataframe_values_are_correct(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_COMMA)
        result = fetch_csv_from_url("https://example.com/data.csv")
        assert result.iloc[0]["name"] == "Alice"
        assert result.iloc[1]["name"] == "Bob"
        assert result.iloc[0]["city"] == "Melbourne"

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_http_error(self, mock_get):
        mock_get.return_value = make_mock_response("Not Found", status_code=404)
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_csv_from_url("https://example.com/data.csv")

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_server_error(self, mock_get):
        mock_get.return_value = make_mock_response("Server Error", status_code=500)
        with pytest.raises(requests.exceptions.HTTPError):
            fetch_csv_from_url("https://example.com/data.csv")

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_raises_on_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_csv_from_url("https://example.com/data.csv")

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_logs_fetch_info(self, mock_get):
        mock_get.return_value = make_mock_response(SAMPLE_CSV_COMMA)
        url = "https://example.com/data.csv"
        with patch("src.data.extractors.support_services_extractor.logger") as mock_logger:
            fetch_csv_from_url(url)
            mock_logger.info.assert_called_once_with(f"Fetching CSV from {url}")

    @patch("src.data.extractors.support_services_extractor.requests.get")
    def test_empty_csv_returns_empty_dataframe(self, mock_get):
        mock_get.return_value = make_mock_response("name,age,city\n")
        result = fetch_csv_from_url("https://example.com/data.csv")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert list(result.columns) == ["name", "age", "city"]