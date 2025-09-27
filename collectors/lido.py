# collectors/lido.py
import requests
from datetime import datetime

def get_lido_staking_rate():
    """
    Простой пример: возвращает APR по stETH (Lido)
    """
    out = []
    try:
        # Lido имеет публичные metrics (см. docs.lido.fi). Примерный URL:
        resp = requests.get("https://stake.lido.fi/api/validators")  # пример
        if resp.status_code == 200:
            data = resp.json()
            # пример: вытаскиваем APR
            apr = data.get("apr", None) or data.get("expectedApy", None)
            if apr is None:
                # fallback manual calc or placeholder
                apr = 0.0
            apr_pct = apr*100 if apr and apr<10 else apr
            out.append({"source": "Lido", "asset": "stETH", "apr": apr_pct, "type":"DeFi", "timestamp": datetime.utcnow()})
    except Exception as e:
        print("Lido error:", e)
    return out
