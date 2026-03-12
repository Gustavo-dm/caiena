import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")

settings = Settings()