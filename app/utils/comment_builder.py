from datetime import datetime

def build_comment(city, weather_data):

    today = datetime.now().strftime("%d/%m")

    text = f"{weather_data['current_temp']}°C e {weather_data['description']} em {city} em {today}. "

    text += "Média para os próximos dias: "

    forecast_text = []

    for date, temp in list(weather_data["forecast"].items())[1:6]:
        
        forecast_text.append(f"{round(temp)}°C em {date}")

    text += ", ".join(forecast_text)

    return text