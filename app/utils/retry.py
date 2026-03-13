import time
import requests


def request_with_retry(url, params, retries=3):

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()

        except requests.RequestException:

            if attempt == retries - 1:
                raise

            time.sleep(1)