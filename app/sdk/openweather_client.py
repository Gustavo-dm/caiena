import requests
from typing import Dict, Any


class OpenWeatherClient:
    """
    Cliente para integração com OpenWeatherMap API.

    Fornece métodos para obter:
    - Clima atual de uma cidade
    - Previsão de 5 dias

    Attributes:
        BASE_URL (str): URL base da API OpenWeatherMap
        api_key (str): Chave de API para autenticação
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """
        Inicializar cliente com chave API.

        Args:
            api_key (str): Chave de API do OpenWeatherMap
        """
        self.api_key = api_key

    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """
        Obter clima atual de uma cidade.

        Args:
            city (str): Nome da cidade

        Returns:
            Dict[str, Any]: Resposta JSON da API contendo:
                - main: temperatura, sensação térmica, umidade
                - weather: descrição do clima
                - wind: velocidade do vento
                - etc.

        Raises:
            requests.exceptions.HTTPError: Se a requisição falhar

        Exemplo:
            >>> client = OpenWeatherClient("your_api_key")
            >>> weather = client.get_current_weather("São Paulo")
            >>> weather["main"]["temp"]
            34.5
        """
        url = f"{self.BASE_URL}/weather"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",  # Retorna temperatura em Celsius
            "lang": "pt_br"      # Descrição em português
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta exceção se status >= 400

        return response.json()

    def get_forecast(self, city: str) -> Dict[str, Any]:
        """
        Obter previsão de 5 dias para uma cidade.

        Args:
            city (str): Nome da cidade

        Returns:
            Dict[str, Any]: Resposta JSON contendo:
                - list: array com previsões (a cada 3 horas)
                  - dt: Unix timestamp
                  - main: temperatura e outros dados
                  - weather: descrição
                  - etc.

        Raises:
            requests.exceptions.HTTPError: Se a requisição falhar

        Exemplo:
            >>> forecast = client.get_forecast("São Paulo")
            >>> len(forecast["list"])  # ~40 entradas (5 dias x ~8 por dia)
            40
        """
        url = f"{self.BASE_URL}/forecast"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Retorna temperatura em Celsius
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()