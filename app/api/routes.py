from fastapi import APIRouter, status, Query, HTTPException
from app.schemas.weather_schema import WeatherCommentRequest, WeatherCommentResponse
from app.services.weather_service import WeatherService
from app.services.gist import GistService
from app.utils.comment_builder import build_comment
from app.sdk.openweather_client import OpenWeatherClient
from app.config import settings

router = APIRouter()

@router.post(
    "/weather-comment",
    response_model=WeatherCommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post weather comment to GitHub Gist",
    description="Fetches weather data for a city and posts it as a comment to a GitHub Gist"
)
def post_weather_comment(
    city: str = Query(..., description="City name", examples="São Paulo"),
    gist_id: str = Query(..., description="GitHub Gist ID", examples="abc123def456")
):
    """
    Post a weather comment to a GitHub Gist.
    
    - **city**: The city name to fetch weather for
    - **gist_id**: The GitHub Gist ID to comment on
    
    Returns a confirmation message with the posted comment text.
    """
    try:
        client = OpenWeatherClient(settings.OPENWEATHER_API_KEY)
        weather_service = WeatherService(client)

        weather_data = weather_service.get_weather_summary(city)

        comment = build_comment(city, weather_data)

        gist_service = GistService(settings.GITHUB_TOKEN)
        gist_service.comment_on_gist(gist_id, comment)

        return WeatherCommentResponse(
            message="Comment posted successfully",
            comment=comment
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing weather comment: {str(e)}"
        )