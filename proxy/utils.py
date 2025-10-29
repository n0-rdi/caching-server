import time
import diskcache

class CachedRequest:
    def __init__(self, body, status, headers, timestamp):
        self.body = body
        self.status = status
        self.headers = headers
        self.timestamp = timestamp

def create_cache(path):
    return diskcache.Cache(path)

def clear_cache(path):
    cache = diskcache.Cache(path)
    cache.clear()
    cache.close()