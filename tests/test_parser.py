from app.utils.parser import calculate_daily_average

def test_average():

    data = {
        "list": [
            {"dt": 1, "main": {"temp": 20}},
            {"dt": 1, "main": {"temp": 30}},
        ]
    }

    result = calculate_daily_average(data)

    assert result is not None