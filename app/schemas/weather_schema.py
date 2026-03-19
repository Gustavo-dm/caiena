from pydantic import BaseModel, Field

class WeatherCommentRequest(BaseModel):
    city: str = Field(..., min_length=1, description="City name", examples=["São Paulo"])
    gist_id: str = Field(..., min_length=1, description="GitHub Gist ID", examples="abc123def456")

    class ConfigDict:
        json_schema_extra = {
            "examples": {
                "city": ["São Paulo"],
                "gist_id": ["abc123def456"]
            }
        }




class WeatherCommentResponse(BaseModel):
    message: str = Field(..., description="Status message", examples=["Comment posted successfully"])
    comment: str = Field(..., description="Comment text posted to gist", examples=["25°C e céu limpo em São Paulo em 13/03..."])