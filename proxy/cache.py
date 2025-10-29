import diskcache


class CachedRequest:
    def __init__(self, body, status, headers, timestamp):
        self.body = body
        self.status = status
        self.headers = headers
        self.timestamp = timestamp


def create_cache(path="./cache"):
    return diskcache.Cache(path)


def clear_cache(path="./cache"):
    cache = diskcache.Cache(path)
    cache.clear()
    print("✅ Cache cleared successfully.")
