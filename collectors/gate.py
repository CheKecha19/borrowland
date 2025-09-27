# collectors/gate.py
from datetime import datetime
from collectors.utils import gate_get

def get_gate_borrow_rates():
    out = []
    try:
        resp = gate_get("/api/v4/margin/loans")
        if resp and resp.status_code == 200:
            data = resp.json()
            for item in data:
                out.append({"exchange": "Gate",
                            "asset": item.get("currency", "").upper(),
                            "apr": float(item.get("interest_rate",0))*100,
                            "timestamp": datetime.utcnow()})
    except Exception as e:
        print("Gate borrow error:", e)
    return out

def get_gate_staking_rates():
    return []  # пока нет данных
