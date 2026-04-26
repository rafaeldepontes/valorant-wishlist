import time
from typing import Dict, Tuple

class IDCache:
    def __init__(self, ttl: int = 900): # 900 seconds = 15 minutes
        self._cache: Dict[str, Tuple[int, float]] = {}
        self.ttl = ttl

    def get(self, uuid_str: str) -> int | None:
        if uuid_str in self._cache:
            internal_id, timestamp = self._cache[uuid_str]
            if time.time() - timestamp < self.ttl:
                return internal_id
            else:
                del self._cache[uuid_str]
        return None

    def set(self, uuid_str: str, internal_id: int):
        self._cache[uuid_str] = (internal_id, time.time())

    def clear(self):
        self._cache.clear()

id_cache = IDCache()
