import unittest
from unittest.mock import patch, MagicMock

from utils.currencies_api import get_currencies


class TestGetCurrencies(unittest.TestCase):

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_ok(self, mock_get):
        # подготавливаем фейковый ответ от API
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
                "EUR": {"Value": 100.7},
            }
        }
        mock_get.return_value = mock_resp

        result = get_currencies(["USD", "EUR"])

        self.assertEqual(result["USD"], 90.5)
        self.assertEqual(result["EUR"], 100.7)
        self.assertEqual(len(result), 2)

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_connection_error(self, mock_get):
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException("network down")

        with self.assertRaises(ConnectionError):
            get_currencies(["USD"])

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_invalid_json(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.side_effect = ValueError("JSON decode error")
        mock_get.return_value = mock_resp

        with self.assertRaises(ValueError):
            get_currencies(["USD"])

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_no_valute_key(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"SomethingElse": {}}
        mock_get.return_value = mock_resp

        with self.assertRaises(KeyError):
            get_currencies(["USD"])

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_missing_currency_code(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
            }
        }
        mock_get.return_value = mock_resp

        with self.assertRaises(KeyError):
            get_currencies(["EUR"])

    @patch("utils.currencies_api.requests.get")
    def test_get_currencies_invalid_value_type(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {
            "Valute": {
                "USD": {"Value": "not-a-number"},
            }
        }
        mock_get.return_value = mock_resp

        with self.assertRaises(TypeError):
            get_currencies(["USD"])


if __name__ == "__main__":
    unittest.main()
