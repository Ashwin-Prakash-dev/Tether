import os
import requests

PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_ENDPOINT = "https://api.pushover.net/1/messages.json"


def push_send(title: str, message: str, priority: int = 0) -> None:
    """
    Pushover Message API:
      token, user, message required; title/priority optional.
    """
    if not PUSHOVER_API_TOKEN or not PUSHOVER_USER_KEY:
        raise RuntimeError("Missing PUSHOVER_API_TOKEN / PUSHOVER_USER_KEY")

    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title[:250] if title else None,
        "message": message[:1024],  
        "priority": priority,
    }
  
    payload = {k: v for k, v in payload.items() if v is not None}

    r = requests.post(PUSHOVER_ENDPOINT, data=payload, timeout=15)
    r.raise_for_status()


def format_whale_alert(t: dict) -> tuple[str, str]:
    title = "Polymarket whale buy (≥$100k)"

    market = t.get("market", "unknown market")
    notional = float(t.get("usd_notional", 0.0))
    ts = t.get("timestamp", "unknown time")
    price = t.get("price")
    size = t.get("size")
    url = t.get("url")

    msg = (
        f"Market: {market}\n"
        f"Est. notional: ${notional:,.0f}\n"
        f"Time (unix): {ts}\n"
    )
    if price is not None:
        msg += f"Price: {price}\n"
    if size is not None:
        msg += f"Size: {size}\n"
    if url:
        msg += url

    return title, msg
