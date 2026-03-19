from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

from app.main import app
from app.sdk.openweather_client import InvalidCityError

client = TestClient(app)


def test_index():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
@patch("app.api.routes.GistService.comment_on_gist")
def test_weather_endpoint_success(mock_gist, mock_weather):
    """Test successful weather comment endpoint"""
    # Mock weather data as AsyncMock since it's async
    mock_weather.return_value = {
        "current_temp": 15,
        "description": "Cloudy",
        "forecast": {"2026-03-14": 16.5, "2026-03-15": 17.2}
    }
    
    # Mock gist comment
    mock_gist.return_value = True

    response = client.post(
        "/weather-comment",
        params={"city": "London", "gist_id": "123"}
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Comment posted successfully"
    assert "comment" in response.json()


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
def test_weather_endpoint_missing_city(mock_weather):
    """Test weather endpoint with missing city parameter"""
    mock_weather.return_value = {
        "current_temp": 15,
        "description": "Cloudy",
        "forecast": {}
    }

    response = client.post(
        "/weather-comment",
        params={"gist_id": "123"}
    )

    assert response.status_code == 422  # Unprocessable Entity


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
def test_weather_endpoint_missing_gist_id(mock_weather):
    """Test weather endpoint with missing gist_id parameter"""
    mock_weather.return_value = {
        "current_temp": 15,
        "description": "Cloudy",
        "forecast": {}
    }

    response = client.post(
        "/weather-comment",
        params={"city": "London"}
    )

    assert response.status_code == 422


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
def test_weather_endpoint_service_error(mock_weather):
    """Test weather endpoint when service raises exception"""
    mock_weather.side_effect = Exception("API Error")

    response = client.post(
        "/weather-comment",
        params={"city": "London", "gist_id": "123"}
    )

    assert response.status_code >= 400


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
def test_weather_endpoint_invalid_city_error(mock_weather):
    """Test weather endpoint with invalid city (returns 400)"""
    mock_weather.side_effect = InvalidCityError("City '123' not found. Please check the spelling and try again.")

    response = client.post(
        "/weather-comment",
        params={"city": "123", "gist_id": "gist123"}
    )

    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@patch("app.api.routes.AsyncWeatherService.get_weather_summary")
def test_weather_endpoint_empty_city(mock_weather):
    """Test weather endpoint with empty city name"""
    mock_weather.side_effect = InvalidCityError("City name cannot be empty")

    response = client.post(
        "/weather-comment",
        params={"city": "", "gist_id": "gist123"}
    )

    # Empty string is caught by FastAPI validation before reaching our code
    # But we test the error handling anyway
    assert response.status_code in [400, 422]