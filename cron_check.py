#!/usr/bin/env python3

import sys
from alerts import push_send, format_whale_alert
from polymarket import fetch_whale_buys
from state import get_redis, is_seen, mark_seen

MIN_CASH_USD = 100_000
LOOKBACK_SECONDS = 3600
SEEN_TTL_SECONDS = 7 * 24 * 3600
LIMIT = 200


def main():
    try:
        print("Starting whale trade check...")
        r = get_redis()
        
        trades = fetch_whale_buys(
            min_cash_usd=MIN_CASH_USD,
            lookback_seconds=LOOKBACK_SECONDS,
            limit=LIMIT,
        )
        
        print(f"Fetched {len(trades)} trades")
        
        alerts_sent = 0
        for t in trades:
            tid = t["trade_id"]
            if is_seen(r, tid):
                continue
            
            mark_seen(r, tid, ttl_seconds=SEEN_TTL_SECONDS)
            
            title, msg = format_whale_alert(t)
            push_send(title, msg, priority=1)
            alerts_sent += 1
            print(f"Alert sent for trade {tid}")
        
        print(f"Check complete. Alerts sent: {alerts_sent}")
        return 0
        
    except Exception as e:
        print(f"Error during check: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
