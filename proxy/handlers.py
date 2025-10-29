import logging
import time
from aiohttp import web
from proxy.models import CachedRequest

async def fetch_from_origin(origin_url, cache, session):
    logging.info("Fetching from origin: %s", origin_url)
    async with session.get(origin_url) as resp:
        headers = dict(resp.headers)
        headers.pop("Transfer-Encoding", None)
        headers.pop("Content-Encoding", None)
        headers.pop("Content-Length", None)
        body = await resp.read()

        cached_resp = CachedRequest(body=body, status=resp.status, headers=headers, timestamp=time.time())
        cache[origin_url] = cached_resp

        headers["X-Cache"] = "MISS"
        return web.Response(body=body, status=resp.status, headers=headers)


async def fetch_from_cache(origin_url, cache):
    logging.info("Fetching from cache: %s", origin_url)
    cached_resp = cache[origin_url]
    headers = dict(cached_resp.headers)
    headers["X-Cache"] = "HIT"
    return web.Response(body=cached_resp.body, status=cached_resp.status, headers=headers)


async def proxy_handler(request):
    cache = request.app["cache"]
    session = request.app["session"]
    ttl = request.app["ttl"]
    origin = request.app["origin"]

    target_path = request.match_info["path"]
    origin_url = f"{origin}/{target_path}"

    cached = cache.get(origin_url)
    if cached and (time.time() - cached.timestamp) < ttl:
        return await fetch_from_cache(origin_url, cache)
    else:
        return await fetch_from_origin(origin_url, cache, session)
