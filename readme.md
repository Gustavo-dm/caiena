# Weather Gist App

API que publica comentários em um Gist com previsão do tempo utilizando OpenWeatherMap.

## Requisitos

- Python 3.11
- OpenWeather API Key
- GitHub Token com acesso a Gist

## Setup

export OPENWEATHER_API_KEY=...
export GITHUB_TOKEN=...

pip install -r requirements.txt

## Rodar

uvicorn app.main:app --reload

## Endpoint

POST /weather-comment

Parametros:

city: nome da cidade
gist_id: id do gist