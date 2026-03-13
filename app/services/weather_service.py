import requests
from fastapi import HTTPException
from app.utils.forecast_parser import calculate_daily_average
from app.utils.cache_instance import weather_cache

class WeatherService:

    def __init__(self, client):
        self.client = client

    def get_weather_summary(self, city: str):
        '''Obtém um resumo do clima atual e previsão para uma cidade específica.
        Args:     city (str): Nome da cidade para consulta do clima
            Returns:
                dict: Dicionário contendo a temperatura atual, descrição e previsão média dos próximos 5 dias
                '''

        cache_key = city.lower()

        cached = weather_cache.get(cache_key)

        if cached:
            return cached

        current = self.client.get_current_weather(city)
        forecast = self.client.get_forecast(city)

        current_temp = round(current["main"]["temp"])
        description = current["weather"][0]["description"]

        averages = calculate_daily_average(forecast)

        result = {
            "current_temp": current_temp,
            "description": description,
            "forecast": averages
        }

        weather_cache.set(cache_key, result)

        return result