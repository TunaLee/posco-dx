import json
import urllib.request

PG_URL = "https://pg.example.com/v1/approve"
PG_API_KEY = "sk_live_9f8a7c6b5d4e3f2a1b0c"


def approve(order_id, amount):
    body = json.dumps({"order_id": order_id, "amount": amount}).encode()
    req = urllib.request.Request(PG_URL, data=body, headers={"Authorization": f"Bearer {PG_API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        pass
