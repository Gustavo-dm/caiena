import time
from app.utils.cache import SimpleCache


def test_cache_set_and_get():

    cache = SimpleCache(ttl=60)

    cache.set("city", {"temp": 30})

    result = cache.get("city")

    assert result["temp"] == 30

def test_cache_expiration():

    cache = SimpleCache(ttl=1)

    cache.set("city", {"temp": 30})

    time.sleep(2)

    result = cache.get("city")

    assert result is None