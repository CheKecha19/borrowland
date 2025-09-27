# collectors/bybit.py
from datetime import datetime
from collectors.utils import bybit_get

def get_bybit_borrow_rates():
    out = []
    try:
        resp = bybit_get("/spot/borrow/borrow-rate")
        if resp and resp.status_code == 200:
            data = resp.json()
            for item in data.get("result", []):
                out.append({"exchange": "Bybit", "asset": item.get("currency").upper(),
                            "apr": float(item.get("rate", 0))*100, "timestamp": datetime.utcnow()})
    except Exception as e:
        print("Bybit borrow error:", e)
    return out

def get_bybit_staking_rates():
    return []  # пока нет публичного endpoint
