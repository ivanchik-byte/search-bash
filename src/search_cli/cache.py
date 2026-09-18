import json
import hashlib
import time
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "search_cli"
CACHE_TTL = 3600 * 12


def clear_cache() -> int:
    if not CACHE_DIR.exists():
        return 0
    count = 0
    for p in CACHE_DIR.glob("*.json"):
        try:
            p.unlink()
            count += 1
        except Exception:
            pass
    return count


def get_cache(key_str: str) -> dict | None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    q_hash = hashlib.sha256(key_str.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{q_hash}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if time.time() - data.get("timestamp", 0) < CACHE_TTL:
                return data.get("result")
        except Exception:
            pass
    return None


def set_cache(key_str: str, result: dict):
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        q_hash = hashlib.sha256(key_str.encode("utf-8")).hexdigest()
        cache_file = CACHE_DIR / f"{q_hash}.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({"timestamp": time.time(), "result": result}, f, ensure_ascii=False)
    except Exception:
        pass
