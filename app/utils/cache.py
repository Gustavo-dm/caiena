import time


class SimpleCache:

    def __init__(self, ttl=600):
        self.ttl = ttl
        self.cache = {}

    def get(self, key):

        item = self.cache.get(key)

        if not item:
            return None

        if time.time() - item["timestamp"] > self.ttl:
            del self.cache[key]
            return None

        return item["data"]

    def set(self, key, value):

        self.cache[key] = {
            "data": value,
            "timestamp": time.time()
        }