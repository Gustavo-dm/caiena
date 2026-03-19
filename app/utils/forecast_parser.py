from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List


def calculate_daily_average(forecast_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calcular a temperatura média diária a partir dos dados de previsão.

    Suporta dois formatos de dados:
    1. dt_txt (string): "2024-12-13 12:00:00"
    2. dt (int): Unix timestamp

    Args:
        forecast_data (Dict[str, Any]): Dados de previsão contendo:
            - list (List): Lista de entradas com temperatura e horário

    Returns:
        Dict[str, int]: Dicionário com datas como chaves (YYYY-MM-DD) 
                       e temperaturas médias como valores (arredondadas)

    Exemplo:
        >>> data = {
        ...     "list": [
        ...         {"dt_txt": "2024-12-13 12:00:00", "main": {"temp": 300}},
        ...         {"dt_txt": "2024-12-13 18:00:00", "main": {"temp": 302}},
        ...         {"dt_txt": "2024-12-14 12:00:00", "main": {"temp": 295}},
        ...     ]
        ... }
        >>> calculate_daily_average(data)
        {'2024-12-13': 301, '2024-12-14': 295}

    Raises:
        KeyError: Se a estrutura de dados não for reconhecida
    """
    daily_temps: Dict[str, List[float]] = defaultdict(list)

    # Processamento de cada entrada de previsão
    for item in forecast_data["list"]:
        # Extrair data em formato string (YYYY-MM-DD)
        if "dt" in item:
            # Formato Unix timestamp
            date = datetime.fromtimestamp(item["dt"]).date()
        elif "dt_txt" in item:
            # Formato string "YYYY-MM-DD HH:MM:SS"
            date = datetime.fromisoformat(item["dt_txt"]).date()
        else:
            raise KeyError("Campo 'dt' ou 'dt_txt' não encontrado nos dados de previsão")

        # Temperatura em Kelvin
        temp = item["main"]["temp"]
        daily_temps[str(date)].append(temp)

    # Calcular média arredondada para cada dia
    averages: Dict[str, int] = {}
    for date, temps in daily_temps.items():
        if len(temps) > 0:
            average_temp = sum(temps) / len(temps)
            averages[date] = round(average_temp)

    return averages