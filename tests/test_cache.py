import time
from app.utils.cache import SimpleCache
import pytest


def test_cache_set_and_get():
    """Test basic cache set and get operations"""
    cache = SimpleCache(ttl=60)
    cache.set("city", {"temp": 30})
    
    result = cache.get("city")
    assert result["temp"] == 30


def test_cache_expiration():
    """Test cache expiration after TTL"""
    cache = SimpleCache(ttl=1)
    cache.set("city", {"temp": 30})
    
    time.sleep(2)
    result = cache.get("city")
    
    assert result is None


def test_cache_multiple_keys():
    """Test cache with multiple keys"""
    cache = SimpleCache(ttl=60)
    
    cache.set("city1", {"temp": 30})
    cache.set("city2", {"temp": 25})
    cache.set("city3", {"temp": 20})
    
    assert cache.get("city1")["temp"] == 30
    assert cache.get("city2")["temp"] == 25
    assert cache.get("city3")["temp"] == 20


def test_cache_overwrite():
    """Test cache value overwrite"""
    cache = SimpleCache(ttl=60)
    
    cache.set("city", {"temp": 30})
    assert cache.get("city")["temp"] == 30
    
    cache.set("city", {"temp": 35})
    assert cache.get("city")["temp"] == 35


def test_cache_nonexistent_key():
    """Test getting nonexistent key returns None"""
    cache = SimpleCache(ttl=60)
    result = cache.get("nonexistent")
    
    assert result is None