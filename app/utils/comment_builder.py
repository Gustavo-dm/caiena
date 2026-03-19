from datetime import datetime
from typing import Dict, Any


def build_comment(city: str, weather_data: Dict[str, Any]) -> str:
    """
    Construir um comentário formatado com informações de clima.

    Args:
        city (str): Nome da cidade
        weather_data (Dict[str, Any]): Dicionário contendo:
            - current_temp (int): Temperatura atual em °C
            - description (str): Descrição do clima (ex: "nublado")
            - forecast (Dict[str, int]): Dicionário com datas e temperaturas médias

    Returns:
        str: Texto formatado para publicação no Gist

    Exemplo:
        >>> data = {
        ...     "current_temp": 34,
        ...     "description": "nublado",
        ...     "forecast": {
        ...         "2026-03-19": 32,
        ...         "2026-03-20": 25,
        ...         "2026-03-21": 29
        ...     }
        ... }
        >>> build_comment("São Paulo", data)
        '34°C e nublado em São Paulo em 19/03. Média para os próximos dias: 32°C em 2026-03-20, 25°C em 2026-03-21, 29°C em 2026-03-22.'
    """
    today = datetime.now().strftime("%d/%m")
    
    # Temperatura atual e descrição do clima
    current_weather = (
        f"{weather_data['current_temp']}°C e {weather_data['description']} em {city} em {today}"
    )
    
    # Preparar previsão dos próximos 5 dias
    # Nota: [1:6] pula o primeiro item (hoje) e pega os próximos 5 dias
    forecast_dates_temps = list(weather_data["forecast"].items())[1:6]
    forecast_lines = [
        f"{round(temp)}°C em {date}" 
        for date, temp in forecast_dates_temps
    ]
    
    # Montagem final do comentário
    comment = f"{current_weather}. Média para os próximos dias: {', '.join(forecast_lines)}."
    
    return comment