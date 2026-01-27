import time
from fastapi import FastAPI
from alerts import push_send, format_whale_alert
from polymarket import fetch_whale_buys
from state import get_redis, is_seen, mark_seen

app = FastAPI(title="Polymarket Whale Alerts")

MIN_CASH_USD = 100_000
LOOKBACK_SECONDS = 300          
SEEN_TTL_SECONDS = 7 * 24 * 3600
LIMIT = 200


@app.get("/health")
def health():
    return {"ok": True, "ts": int(time.time())}


@app.get("/check")
def check():
    r = get_redis()

    trades = fetch_whale_buys(
        min_cash_usd=MIN_CASH_USD,
        lookback_seconds=LOOKBACK_SECONDS,
        limit=LIMIT,
    )

    alerts_sent = 0
    for t in trades:
        tid = t["trade_id"]
        if is_seen(r, tid):
            continue

        mark_seen(r, tid, ttl_seconds=SEEN_TTL_SECONDS)

        title, msg = format_whale_alert(t)
        push_send(title, msg, priority=1)
        alerts_sent += 1

    return {"ok": True, "checked_trades": len(trades), "alerts_sent": alerts_sent}
