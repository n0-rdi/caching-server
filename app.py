import logging
import aiohttp
from aiohttp import web
import argparse
import time

class CachedRequest:
    def __init__(self, body, status, headers, timestamp):
        self.body = body
        self.status = status
        self.headers = headers
        self.timestamp = time.time()

async def return_from_cache(url, cache):
    print("Returning from cache")
    cached_resp = cache[url]
    return web.Response(body = cached_resp.body, status = cached_resp.status, headers = cached_resp.headers)

async def return_new(url, cache):
    print("Returning from new")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            headers = dict(resp.headers)
            headers.pop("Transfer-Encoding", None)
            logging.info(f"headers: {headers}")
            body = await resp.read()

            rq = CachedRequest(body, resp.status, headers, time.time())
            cache[url] = rq

            return web.Response(body=body, status=resp.status, headers=headers)

async def proxy(request):
    cache = request.app["cache"]
    session = request.app["session"]
    ttl = request.app["ttl"]

    target_url = request.query['url']

    if target_url in cache and (time.time() - cache[target_url].timestamp) < ttl:
        return await return_from_cache(target_url, cache)
    else:
        return await return_new(target_url, cache)

async def create_app(args):
    app = web.Application()
    app.add_routes([web.get('/', proxy)])
    app["cache"] = {}
    app["session"] = aiohttp.ClientSession()
    app["ttl"] = args.ttl

    async def close_session():
        await app["session"].close()
    app.on_cleanup.append(close_session)

    return app

def parse_args():
    parser = argparse.ArgumentParser(description='caching proxy server')
    parser.add_argument('-p', '--port', default=8080, type=int, help='the port on which the caching proxy server will run')
    parser.add_argument('-o', '--origin', default='http://localhost:8080', help='the URL of the server to which the requests will be forwarded')
    parser.add_argument('-t', '--ttl', default=600, type=float, help='cache lifetime in seconds')
    return parser.parse_args()

def main():
    args = parse_args()
    web.run_app(create_app(args), port = args.port)

if __name__ == '__main__':
    main()