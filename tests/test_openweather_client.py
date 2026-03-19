from unittest.mock import patch, MagicMock
import pytest
import requests

from app.sdk.openweather_client import OpenWeatherClient


class TestOpenWeatherClient:
    """Test suite for OpenWeatherClient"""

    def test_client_initialization(self):
        """Test OpenWeatherClient initialization"""
        api_key = "test_api_key_12345"
        client = OpenWeatherClient(api_key)
        
        assert client.api_key == api_key
        assert client.BASE_URL == "https://api.openweathermap.org/data/2.5"

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_current_weather_success(self, mock_get):
        """Test successful current weather retrieval"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "main": {"temp": 25, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 5}
        }
        mock_get.return_value = mock_response

        client = OpenWeatherClient("test_key")
        result = client.get_current_weather("London")

        assert result["main"]["temp"] == 25
        assert result["weather"][0]["description"] == "clear sky"
        mock_get.assert_called_once()

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_current_weather_api_error(self, mock_get):
        """Test current weather retrieval with API error"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        client = OpenWeatherClient("test_key")
        
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_current_weather("InvalidCity")

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_current_weather_parameters(self, mock_get):
        """Test correct parameters are sent to API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"main": {"temp": 20}, "weather": [{"description": "cloudy"}]}
        mock_get.return_value = mock_response

        client = OpenWeatherClient("my_api_key")
        client.get_current_weather("Paris")

        # Verify the correct URL was called
        call_args = mock_get.call_args
        assert "weather" in call_args[0][0]
        assert call_args[1]["params"]["q"] == "Paris"
        assert call_args[1]["params"]["appid"] == "my_api_key"
        assert call_args[1]["params"]["units"] == "metric"
        assert call_args[1]["params"]["lang"] == "pt_br"

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_forecast_success(self, mock_get):
        """Test successful forecast retrieval"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "list": [
                {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 20}},
                {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 18}},
                {"dt_txt": "2024-12-14 00:00:00", "main": {"temp": 16}},
            ]
        }
        mock_get.return_value = mock_response

        client = OpenWeatherClient("test_key")
        result = client.get_forecast("Berlin")

        assert len(result["list"]) == 3
        assert result["list"][0]["main"]["temp"] == 20
        mock_get.assert_called_once()

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_forecast_api_error(self, mock_get):
        """Test forecast retrieval with API error"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response

        client = OpenWeatherClient("invalid_key")
        
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_forecast("London")

    @patch("app.sdk.openweather_client.requests.get")
    def test_get_forecast_parameters(self, mock_get):
        """Test correct parameters are sent to forecast API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"list": []}
        mock_get.return_value = mock_response

        client = OpenWeatherClient("my_api_key")
        client.get_forecast("Madrid")

        call_args = mock_get.call_args
        assert "forecast" in call_args[0][0]
        assert call_args[1]["params"]["q"] == "Madrid"
        assert call_args[1]["params"]["appid"] == "my_api_key"
        assert call_args[1]["params"]["units"] == "metric"
        # Note: lang parameter is not included in forecast endpoint
