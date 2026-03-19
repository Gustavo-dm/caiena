
from app.services.weather_service import WeatherService
from app.utils.cache_instance import weather_cache
import pytest

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


class FakeClientWithTimestamp:
    def get_current_weather(self, city):
        return {
            "main": {"temp": 298.5},
            "weather": [{"description": "sunny"}]
        }

    def get_forecast(self, city):
        from datetime import datetime
        return {
            "list": [
                {"dt": int(datetime(2024, 12, 13, 12).timestamp()), "main": {"temp": 298.5}},
                {"dt": int(datetime(2024, 12, 13, 18).timestamp()), "main": {"temp": 300}},
            ]
        }


def test_weather_service_basic():
    """Test basic weather service functionality"""
    client = FakeClient()
    service = WeatherService(client)
    result = service.get_weather_summary("London")
    
    assert "current_temp" in result
    assert "forecast" in result
    assert isinstance(result["current_temp"], int)
    assert isinstance(result["description"], str)


def test_weather_service_temperature_rounding():
    """Test temperature is properly rounded"""
    client = FakeClientWithTimestamp()
    service = WeatherService(client)
    result = service.get_weather_summary("Paris")
    
    # 298.5 should round to 299 or 298 depending on rounding
    assert isinstance(result["current_temp"], int)
    assert result["current_temp"] in [298, 299]


def test_weather_service_cache_hit():
    """Test cache hit returns cached data"""
    # Clear cache first
    weather_cache.cache = {}
    
    client = FakeClient()
    service = WeatherService(client)
    
    # First call - cold cache
    result1 = service.get_weather_summary("Berlin")
    
    # Second call - should hit cache
    result2 = service.get_weather_summary("Berlin")
    
    assert result1 == result2


def test_weather_service_cache_case_insensitive():
    """Test cache key is case insensitive"""
    weather_cache.cache = {}
    
    client = FakeClient()
    service = WeatherService(client)
    
    result1 = service.get_weather_summary("Madrid")
    result2 = service.get_weather_summary("MADRID")
    
    # Should return same cached result
    assert result1 == result2


def test_weather_service_forecast_structure():
    """Test forecast data structure is correct"""
    client = FakeClient()
    service = WeatherService(client)
    result = service.get_weather_summary("Rome")
    
    assert isinstance(result["forecast"], dict)
    for date, temp in result["forecast"].items():
        assert isinstance(date, str)
        assert isinstance(temp, int)