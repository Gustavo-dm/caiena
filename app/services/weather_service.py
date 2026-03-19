import requests
from fastapi import HTTPException
from typing import Dict, Any
from app.sdk.openweather_client import OpenWeatherClient
from app.utils.forecast_parser import calculate_daily_average
from app.utils.cache_instance import weather_cache


class WeatherService:
    """
    Serviço para obter informações de clima com cache.

    Responsabilidades:
    - Buscar dados de temperatura atual via OpenWeatherClient
    - Buscar previsão para os próximos dias
    - Calcular média de temperaturas por dia
    - Gerenciar cache para evitar múltiplas chamadas à API

    Attributes:
        client (OpenWeatherClient): Cliente para acessar OpenWeather API
    """

    def __init__(self, client: OpenWeatherClient):
        """
        Inicializar serviço de clima.

        Args:
            client (OpenWeatherClient): Cliente configurado com API key
        """
        self.client = client

    def get_weather_summary(self, city: str) -> Dict[str, Any]:
        """
        Obter resumo do clima atual e previsão para uma cidade.

        Fluxo:
        1. Verifica se dados estão no cache
        2. Se cache miss, consulta OpenWeather API
        3. Calcula média diária da previsão
        4. Armazena dados em cache com TTL

        Args:
            city (str): Nome da cidade para consulta

        Returns:
            Dict[str, Any]: Dicionário com:
                - current_temp (int): Temperatura atual em °C
                - description (str): Descrição do clima (ex: "céu limpo")
                - forecast (Dict[str, int]): Datas e temperaturas médias

        Exemplo:
            >>> service = WeatherService(client)
            >>> result = service.get_weather_summary("São Paulo")
            >>> result
            {
                'current_temp': 34,
                'description': 'nublado',
                'forecast': {
                    '2026-03-19': 32,
                    '2026-03-20': 25,
                    '2026-03-21': 29
                }
            }

        Raises:
            HTTPException: Se a API retorna erro (ex: cidade não encontrada)
        """
        cache_key = city.lower()

        # Verificar cache
        cached = weather_cache.get(cache_key)
        if cached:
            return cached

        # Chamar APIs externas
        current = self.client.get_current_weather(city)
        forecast = self.client.get_forecast(city)

        # Extrair temperatura atual e descrição
        current_temp = round(current["main"]["temp"])
        description = current["weather"][0]["description"]

        # Calcular média diária da previsão
        averages = calculate_daily_average(forecast)

        # Estruturar resultado
        result = {
            "current_temp": current_temp,
            "description": description,
            "forecast": averages
        }

        # Armazenar em cache
        weather_cache.set(cache_key, result)

        return result