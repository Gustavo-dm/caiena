from collections import defaultdict
from datetime import datetime

def calculate_daily_average(forecast_data):

    daily_temps = defaultdict(list)

    for item in forecast_data["list"]:
        date = datetime.fromtimestamp(item["dt"]).date()
        temp = item["main"]["temp"]

        daily_temps[date].append(temp)

    averages = {}

    for date, temps in daily_temps.items():
        averages[date] = sum(temps) / len(temps)

    return averages