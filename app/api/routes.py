from fastapi import APIRouter
from app.services.weather import WeatherService
from app.services.gist import GistService
from app.utils.comment_builder import build_comment
from app.sdk.openweather_client import OpenWeatherClient
from app.config import settings

router = APIRouter()

@router.post("/weather-comment")

def post_weather_comment(city: str, gist_id: str):

    client = OpenWeatherClient(settings.OPENWEATHER_API_KEY)
    weather_service = WeatherService(client)

    weather_data = weather_service.get_weather_summary(city)

    comment = build_comment(city, weather_data)

    gist_service = GistService(settings.GITHUB_TOKEN)
    gist_service.comment_on_gist(gist_id, comment)

    return {
        "message": "Comment posted successfully",
        "comment": comment
    }