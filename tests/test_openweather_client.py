from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import httpx

from app.sdk.openweather_client import AsyncOpenWeatherClient


class TestAsyncOpenWeatherClient:
    """Test suite for AsyncOpenWeatherClient"""

    def test_client_initialization(self):
        """Test AsyncOpenWeatherClient initialization"""
        api_key = "test_api_key_12345"
        client = AsyncOpenWeatherClient(api_key)
        
        assert client.api_key == api_key
        assert client.BASE_URL == "https://api.openweathermap.org/data/2.5"

    @pytest.mark.asyncio
    async def test_get_current_weather_success(self):
        """Test successful current weather retrieval"""
        # Note: raise_for_status() and json() are sync methods even with AsyncClient
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "main": {"temp": 25, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 5}
        }
        mock_response.raise_for_status.return_value = None

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("test_key")
            result = await client.get_current_weather("London")

            assert result["main"]["temp"] == 25
            assert result["weather"][0]["description"] == "clear sky"
            mock_async_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_weather_api_error(self):
        """Test current weather retrieval with API error"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("404 Not Found")

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("test_key")
            
            with pytest.raises(httpx.HTTPError):
                await client.get_current_weather("InvalidCity")

    @pytest.mark.asyncio
    async def test_get_current_weather_parameters(self):
        """Test correct parameters are sent to API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"main": {"temp": 20}, "weather": [{"description": "cloudy"}]}
        mock_response.raise_for_status.return_value = None

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("my_api_key")
            await client.get_current_weather("Paris")

            # Verify the correct parameters were called
            call_args = mock_async_client.get.call_args
            assert "weather" in call_args[0][0]
            assert call_args[1]["params"]["q"] == "Paris"
            assert call_args[1]["params"]["appid"] == "my_api_key"
            assert call_args[1]["params"]["units"] == "metric"
            assert call_args[1]["params"]["lang"] == "pt_br"

    @pytest.mark.asyncio
    async def test_get_forecast_success(self):
        """Test successful forecast retrieval"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "list": [
                {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 20}},
                {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 18}},
                {"dt_txt": "2024-12-14 00:00:00", "main": {"temp": 16}},
            ]
        }
        mock_response.raise_for_status.return_value = None

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("test_key")
            result = await client.get_forecast("Berlin")

            assert len(result["list"]) == 3
            assert result["list"][0]["main"]["temp"] == 20

    @pytest.mark.asyncio
    async def test_get_forecast_api_error(self):
        """Test forecast retrieval with API error"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("401 Unauthorized")

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("invalid_key")
            
            with pytest.raises(httpx.HTTPError):
                await client.get_forecast("London")

    @pytest.mark.asyncio
    async def test_get_forecast_parameters(self):
        """Test correct parameters are sent to forecast API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"list": []}
        mock_response.raise_for_status.return_value = None

        with patch("app.sdk.openweather_client.httpx.AsyncClient") as mock_client_class:
            mock_async_client = AsyncMock()
            mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
            mock_async_client.__aexit__ = AsyncMock(return_value=None)
            mock_async_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_async_client

            client = AsyncOpenWeatherClient("my_api_key")
            await client.get_forecast("Madrid")

            call_args = mock_async_client.get.call_args
            assert "forecast" in call_args[0][0]
            assert call_args[1]["params"]["q"] == "Madrid"
            assert call_args[1]["params"]["appid"] == "my_api_key"
            assert call_args[1]["params"]["units"] == "metric"
