from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200


@patch("app.services.weather.WeatherService.get_weather_summary")
@patch("app.services.gist.GistService.comment_on_gist")
def test_weather_endpoint(mock_gist, mock_weather):
    # Mock weather data
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