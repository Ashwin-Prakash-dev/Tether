import os
import redis

REDIS_URL = os.getenv("https://fitting-fawn-21199.upstash.io")


def get_redis() -> "redis.Redis":
    if not REDIS_URL:
        raise RuntimeError("Missing REDIS_URL")
    return redis.from_url(REDIS_URL, decode_responses=True)


def seen_key(trade_id: str) -> str:
    return f"seen:{trade_id}"


def is_seen(r: "redis.Redis", trade_id: str) -> bool:
    return r.exists(seen_key(trade_id)) == 1


def mark_seen(r: "redis.Redis", trade_id: str, ttl_seconds: int) -> None:
    # Mark first to prevent duplicate alerts if overlapping cron hits occur.
    r.set(seen_key(trade_id), "1", ex=ttl_seconds)
