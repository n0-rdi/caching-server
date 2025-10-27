#  Caching Proxy Server (Python + aiohttp)

A simple **CLI-based caching proxy server** built with `aiohttp`.  
It forwards incoming HTTP requests to a specified origin server, caches the responses on a disk,  
and serves subsequent identical requests directly from cache to reduce load and latency.

# Implementation of https://roadmap.sh/projects/caching-server

---

## 🚀 Features

- ✅ Forwards HTTP requests to an origin server  
- 💾 Caches responses on disk using `diskcache`  
- 🕒 Configurable cache lifetime (TTL)  
- ⚡ Adds headers indicating cache status  
  - `X-Cache: HIT` → response served from cache  
  - `X-Cache: MISS` → response fetched from origin  
- 🧹 Cache clearing via CLI flag  
- 🛠 Simple and lightweight — for educational or development use

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/caching-proxy-server.git
cd caching-proxy-server
pip install -r requirements.txt
````

Usage:
````bash
python proxy.py --port 3000 --origin https://dummyjson.com
````

⚠️ Notes

The --origin URL must not point to the same host/port as the proxy
(e.g., don’t use --origin http://localhost:8080 while proxy runs on port 8080) —
this will cause an infinite proxy loop.

Only GET requests are cached by default.

The cache uses diskcache for persistence between runs.

