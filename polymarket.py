import time
import requests

DATA_API_TRADES = "https://data-api.polymarket.com/trades"


def fetch_whale_buys(
    min_cash_usd: float = 100_000,
    lookback_seconds: int = 3600,
    limit: int = 200,
) -> list[dict]:

    now = int(time.time())
    since = now - lookback_seconds

    params = {
        "side": "BUY",
        "filterType": "CASH",
        "filterAmount": str(int(min_cash_usd)),
        "limit": limit,
        "offset": 0,
    }

    print("Polymarket params:", params)

    r = requests.get(DATA_API_TRADES, params=params, timeout=15)
    r.raise_for_status()
    rows = r.json()

    out: list[dict] = []
    for row in rows:
        ts = row.get("timestamp")
        try:
            ts_int = int(float((ts)))
        except Exception:
            ts_int = None

        if ts_int is not None and ts_int < since:
            continue

        trade_id = str(row.get("transactionHash") or row.get("id") or "")
        if not trade_id:
            
            trade_id = f"{row.get('proxyWallet','')}-{ts}-{row.get('slug','')}-{row.get('size','')}-{row.get('price','')}"

        title = row.get("title") or row.get("slug") or "Polymarket"
        outcome = row.get("outcome")
        market_name = f"{title}" + (f" — {outcome}" if outcome else "")

        price = row.get("price")
        size = row.get("size")
        usd_notional = None
        try:
            if price is not None and size is not None:
                usd_notional = float(price) * float(size)
        except Exception:
            usd_notional = None

        event_slug = row.get("eventSlug")
        url = f"https://polymarket.com/event/{event_slug}" if event_slug else None

        out.append(
            {
                "trade_id": trade_id,
                "market": market_name,
                "timestamp": ts_int or ts,
                "price": price,
                "size": size,
                "usd_notional": float(usd_notional) if usd_notional is not None else float(min_cash_usd),
                "url": url,
                "raw": row,
            }
        )

    return out
