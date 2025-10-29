import argparse


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
