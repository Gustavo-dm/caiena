from collections import defaultdict
from datetime import datetime

def calculate_daily_average(forecast_data):
    '''Calcula a temperatura média diária a partir dos dados de previsão do tempo.
    Args:
        forecast_data (dict): Dados de previsão do tempo obtidos da API
            Returns:
                dict: Dicionário com as datas como chaves e as temperaturas médias como valores
                '''

    daily_temps = defaultdict(list)

    for item in forecast_data["list"]:

        if "dt" in item:
            date = datetime.fromtimestamp(item["dt"]).date()
        else:
            date = datetime.fromisoformat(item["dt_txt"]).date()

        temp = item["main"]["temp"]

        daily_temps[date].append(temp)

    averages = {}

    for date, temps in daily_temps.items():
        averages[str(date)] = round(sum(temps) / len(temps))

    return averages