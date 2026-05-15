import pytest
from unittest.mock import MagicMock, patch

from src.services.personalisation_service import extract_preferences, _EMPTY_PREFERENCES


class TestExtractPreferences:
    def test_empty_string_returns_empty_preferences(self):
        result = extract_preferences("")
        assert result == _EMPTY_PREFERENCES

    def test_none_returns_empty_preferences(self):
        result = extract_preferences(None)
        assert result == _EMPTY_PREFERENCES

    def test_whitespace_only_returns_empty_preferences(self):
        result = extract_preferences("   ")
        assert result == _EMPTY_PREFERENCES

    def test_no_api_key_returns_empty_preferences(self):
        with patch("src.services.personalisation_service.os.environ.get", return_value=None):
            result = extract_preferences("I love seafood")
        assert result == _EMPTY_PREFERENCES

    def test_no_api_key_logs_warning(self):
        with patch("src.services.personalisation_service.os.environ.get", return_value=None), \
             patch("src.services.personalisation_service.logger") as mock_logger:
            extract_preferences("I love seafood")
        mock_logger.warning.assert_called_once()

    def test_valid_response_parsed_correctly(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            '{"preferred_sub_categories": ["Seafood"], '
            '"nutrient_priorities": ["protein_g"], '
            '"avoid_sub_categories": ["Pork"]}'
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I love seafood, avoid pork, want protein")

        assert result["preferred_sub_categories"] == ["Seafood"]
        assert result["nutrient_priorities"] == ["protein_g"]
        assert result["avoid_sub_categories"] == ["Pork"]

    def test_markdown_fenced_json_parsed_correctly(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "```json\n"
            '{"preferred_sub_categories": ["Vegetables"], '
            '"nutrient_priorities": [], '
            '"avoid_sub_categories": []}\n'
            "```"
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I eat lots of vegetables")

        assert result["preferred_sub_categories"] == ["Vegetables"]

    def test_api_exception_returns_empty_preferences(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Connection error")

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I love seafood")

        assert result == _EMPTY_PREFERENCES

    def test_api_exception_does_not_raise(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = RuntimeError("timeout")

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I love seafood")

        assert result is not None

    def test_invalid_json_returns_empty_preferences(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "not valid json at all"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I love seafood")

        assert result == _EMPTY_PREFERENCES

    def test_result_always_has_all_three_keys(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"preferred_sub_categories": ["Fruit"]}'
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I like fruit")

        assert "preferred_sub_categories" in result
        assert "nutrient_priorities" in result
        assert "avoid_sub_categories" in result

    def test_description_truncated_to_300_chars(self):
        long_desc = "x" * 500
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            '{"preferred_sub_categories": [], "nutrient_priorities": [], "avoid_sub_categories": []}'
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            extract_preferences(long_desc)

        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args.kwargs["messages"][1]["content"]
        assert len(user_message) <= 300

    def test_groq_not_installed_returns_empty(self):
        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", None), \
             patch("src.services.personalisation_service.logger") as mock_logger:
            result = extract_preferences("I like vegetables")
        assert result == _EMPTY_PREFERENCES
        mock_logger.warning.assert_called()

    def test_markdown_fence_without_json_header_still_parsed(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = (
            "```\n"
            '{"preferred_sub_categories": ["Fruit"], "nutrient_priorities": [], "avoid_sub_categories": []}'
            "\n```"
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch("src.services.personalisation_service.os.environ.get", return_value="fake-key"), \
             patch("src.services.personalisation_service.Groq", return_value=mock_client):
            result = extract_preferences("I like fruit")

        assert result["preferred_sub_categories"] == ["Fruit"]
