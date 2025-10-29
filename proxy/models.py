from dataclasses import dataclass

@dataclass
class CachedRequest:
    status: int
    headers: dict
    body: bytes
    timestamp: float