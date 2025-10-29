import logging
from aiohttp import web
from proxy.app import create_app
from proxy.config import parse_args
from proxy.cache import clear_cache


def main():
    args = parse_args()

    if args.clear_cache:
        clear_cache()
        return

    logging.basicConfig(
        level=logging.INFO,
        filename="proxy.log",
        filemode="w",
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    app = create_app(args)
    web.run_app(app, port=args.port)


if __name__ == "__main__":
    main()
