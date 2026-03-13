from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_index():

    response = client.get("/")

    assert response.status_code == 200


@patch("app.services.gist.GistService.publish_comment")
def test_weather_endpoint(mock_publish):

    mock_publish.return_value = True

    response = client.post(
        "/weather-comment",
        params={"city": "London", "gist_id": "123"}
    )

    assert response.status_code == 200