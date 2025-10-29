import aiohttp
from aiohttp import web
from .cache import create_cache
from .handlers import proxy_handler


async def create_app(args):
    app = web.Application()
    app["cache"] = create_cache()
    app["session"] = aiohttp.ClientSession()
    app["ttl"] = args.ttl
    app["origin"] = args.origin.rstrip("/")

    app.router.add_route("GET", "/{path:.*}", proxy_handler)

    async def close_session(_):
        await app["session"].close()

    app.on_cleanup.append(close_session)
    return app
