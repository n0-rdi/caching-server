import logging
import aiohttp
from aiohttp import web
import argparse
import time
import sys
import diskcache

class CachedRequest:
    def __init__(self, body, status, headers, timestamp):
        self.body = body
        self.status = status
        self.headers = headers
        self.timestamp = timestamp


async def fetch_from_origin(origin_url, cache, session):
    print(f"Fetching from origin: {origin_url}")
    async with session.get(origin_url) as resp:
        headers = dict(resp.headers)
        headers.pop("Transfer-Encoding", None)
        headers.pop("Content-Encoding", None)
        headers.pop("Content-Length", None)
        body = await resp.read()

        cached_resp = CachedRequest(body, resp.status, headers, time.time())
        cache[origin_url] = cached_resp

        headers["X-Cache"] = "MISS"

        return web.Response(body=body, status=resp.status, headers=headers)


async def fetch_from_cache(origin_url, cache):
    print(f"Returning from cache: {origin_url}")
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


async def create_app(args):
    app = web.Application()
    app["cache"] = diskcache.Cache("./cache")
    app["session"] = aiohttp.ClientSession()
    app["ttl"] = args.ttl
    app["origin"] = args.origin.rstrip("/")

    app.router.add_route("GET", "/{path:.*}", proxy_handler)

    async def close_session():
        await app["session"].close()
    app.on_cleanup.append(close_session)

    return app


def parse_args():
    parser = argparse.ArgumentParser(description="Caching proxy server")
    parser.add_argument("--port", "-p", type=int, default=8080,
                        help="Port to run the caching proxy server")
    parser.add_argument("--origin", "-o", required=False,
                        default="http://localhost:3000",
                        help="Origin server to forward requests to")
    parser.add_argument("--ttl", "-t", type=float, default=600,
                        help="Cache lifetime in seconds")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Clear the cache and exit")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.clear_cache:
        cache = diskcache.Cache("./cache")
        cache.clear()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    app = create_app(args)
    web.run_app(app, port=args.port)


if __name__ == "__main__":
    main()
