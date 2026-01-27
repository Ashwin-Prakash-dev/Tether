import os
import redis

REDIS_URL = os.getenv("REDIS_URL")


def get_redis() -> "redis.Redis":
    if not REDIS_URL:
        raise RuntimeError("Missing REDIS_URL")
    return redis.from_url(REDIS_URL, decode_responses=True)


def seen_key(trade_id: str) -> str:
    return f"seen:{trade_id}"


def is_seen(r: "redis.Redis", trade_id: str) -> bool:
    return r.exists(seen_key(trade_id)) == 1


def mark_seen(r: "redis.Redis", trade_id: str, ttl_seconds: int) -> None:
    r.set(seen_key(trade_id), "1", ex=ttl_seconds)
