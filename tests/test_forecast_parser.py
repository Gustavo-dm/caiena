from app.utils.forecast_parser import calculate_daily_average


def test_calculate_daily_average():

    fake_forecast = {
        "list": [
            {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 300}},
            {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 302}},
            {"dt_txt": "2024-12-14 12:00:00", "main": {"temp": 295}},
        ]
    }

    result = calculate_daily_average(fake_forecast)

    assert len(result) == 2