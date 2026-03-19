from app.utils.forecast_parser import calculate_daily_average
from datetime import datetime
import pytest


def test_calculate_daily_average_datetime_string():
    """Test with datetime string format (dt_txt)"""
    fake_forecast = {
        "list": [
            {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 300}},
            {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 302}},
            {"dt_txt": "2024-12-14 12:00:00", "main": {"temp": 295}},
        ]
    }
    result = calculate_daily_average(fake_forecast)
    
    assert len(result) == 2
    assert "2024-12-13" in result
    assert "2024-12-14" in result
    # Average for 2024-12-13: (300 + 302) / 2 = 301
    assert result["2024-12-13"] == 301
    # Average for 2024-12-14: 295 / 1 = 295
    assert result["2024-12-14"] == 295


def test_calculate_daily_average_unix_timestamp():
    """Test with unix timestamp format (dt)"""
    fake_forecast = {
        "list": [
            {"dt": int(datetime(2024, 12, 13, 12).timestamp()), "main": {"temp": 300}},
            {"dt": int(datetime(2024, 12, 13, 18).timestamp()), "main": {"temp": 302}},
            {"dt": int(datetime(2024, 12, 14, 12).timestamp()), "main": {"temp": 295}},
        ]
    }
    result = calculate_daily_average(fake_forecast)
    
    assert len(result) == 2
    assert "2024-12-13" in result
    assert result["2024-12-13"] == 301


def test_calculate_daily_average_single_entry_per_day():
    """Test with single temperature entry per day"""
    fake_forecast = {
        "list": [
            {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 300}},
            {"dt_txt": "2024-12-14 12:00:00", "main": {"temp": 295}},
        ]
    }
    result = calculate_daily_average(fake_forecast)
    
    assert len(result) == 2
    assert result["2024-12-13"] == 300
    assert result["2024-12-14"] == 295


def test_calculate_daily_average_empty_list():
    """Test with empty forecast list"""
    fake_forecast = {"list": []}
    result = calculate_daily_average(fake_forecast)
    
    assert len(result) == 0


def test_calculate_daily_average_rounding():
    """Test temperature rounding behavior"""
    fake_forecast = {
        "list": [
            {"dt_txt": "2024-12-13 00:00:00", "main": {"temp": 300.1}},
            {"dt_txt": "2024-12-13 06:00:00", "main": {"temp": 301.9}},
        ]
    }
    result = calculate_daily_average(fake_forecast)
    
    # Average: (300.1 + 301.9) / 2 = 301.0, rounded to 301
    assert result["2024-12-13"] == 301