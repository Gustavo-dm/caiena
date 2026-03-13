
from app.services.weather_service import WeatherService

class FakeClient:

    def get_current_weather(self, city):
        return {
            "main": {"temp": 300},
            "weather": [{"description": "cloudy"}]
        }

    def get_forecast(self, city):
        return {
            "list": [
                {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 300}},
                {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 302}},
            ]
        }


def test_weather_service():

    client = FakeClient()

    service = WeatherService(client)

    result = service.get_weather_summary("London")

    assert "current_temp" in result
    assert "forecast" in result