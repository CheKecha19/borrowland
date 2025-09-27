# collectors/kucoin.py
from datetime import datetime
from collectors.utils import kucoin_get

def get_kucoin_borrow_rates():
    out = []
    try:
        resp = kucoin_get("/api/v1/margin/config")
        if resp and resp.status_code == 200:
            data = resp.json()
            for item in data.get("data", []):
                out.append({"exchange": "KuCoin",
                            "asset": item.get("currency", "").upper(),
                            "apr": float(item.get("interestRate",0))*100,
                            "timestamp": datetime.utcnow()})
    except Exception as e:
        print("KuCoin borrow error:", e)
    return out

def get_kucoin_staking_rates():
    return []  # нет данных для staking
