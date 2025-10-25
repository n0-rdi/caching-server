import logging
import aiohttp
from aiohttp import web
import argparse

async def proxy(request):
    target_url = request.query['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as resp:
            headers = dict(resp.headers)
            headers.pop("Transfer-Encoding", None)
            logging.info(f"headers: {headers}")
            body = await resp.read()

            return web.Response(body=body,
                            status=resp.status,
                            headers=headers
                                )

app = web.Application()
app.router.add_get('/', proxy)

def parse_args():
    parser = argparse.ArgumentParser(description='caching proxy server')
    parser.add_argument('-p', '--port', default=8080, type=int, help='the port on which the caching proxy server will run')
    parser.add_argument('-o', '--origin', default='http://localhost:8080', help='the URL of the server to which the requests will be forwarded')

    return parser.parse_args()

def main():
    args = parse_args()
    web.run_app(app, port=args.port, origin=args.origin)



if __name__ == '__main__':
    main()