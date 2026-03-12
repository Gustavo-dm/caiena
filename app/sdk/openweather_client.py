import requests


class OpenWeatherClient:

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, city):

        url = f"{self.BASE_URL}/weather"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br"
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        return response.json()

    def get_forecast(self, city):

        url = f"{self.BASE_URL}/forecast"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        return response.json()