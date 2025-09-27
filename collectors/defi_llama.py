# collectors/defi_llama.py
import requests
from datetime import datetime

BASE = "https://yields.llama.fi"

def get_defi_llama_yields():
    """
    Возвращает список {source, asset, apr, type, timestamp}
    DeFi Llama /yields endpoint возвращает информацию по множеству стратегий
    """
    out = []
    try:
        resp = requests.get(f"{BASE}/v1/pools")  # endpoint примерный, проверь текущие доки
        if resp.status_code == 200:
            data = resp.json()
            # data — dict of pools; нужно привести к нашим полям
            for pool in data:
                # примерный формат
                asset = pool.get("symbol") or pool.get("rewardTokens", [])
                apr = pool.get("apy") or pool.get("apyBase") or 0
                # normalize to percent
                apr_pct = apr*100 if apr and apr < 10 else apr
                out.append({"source": "DeFiLlama", "asset": pool.get("symbol", "UNKNOWN"), "apr": apr_pct, "type":"DeFi", "timestamp": datetime.utcnow()})
    except Exception as e:
        print("DeFi Llama error:", e)
    return out
