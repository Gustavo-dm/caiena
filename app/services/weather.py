from app.utils.parser import calculate_daily_average

class WeatherService:

    def __init__(self, client):
        self.client = client

    def get_weather_summary(self, city):

        current = self.client.get_current_weather(city)
        forecast = self.client.get_forecast(city)

        current_temp = round(current["main"]["temp"])
        description = current["weather"][0]["description"]

        averages = calculate_daily_average(forecast)

        return {
            "current_temp": current_temp,
            "description": description,
            "forecast": averages
        }