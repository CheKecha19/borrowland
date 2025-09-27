# collectors/defi.py
import requests
from datetime import datetime

def get_defillama_staking_rates(limit=20):
    """
    Берём топ стейкинг-пулы с DefiLlama
    """
    out = []
    try:
        url = "https://yields.llama.fi/pools"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            pools = data.get("data", [])
            for item in pools[:limit]:  # берём только первые limit
                symbol = item.get("symbol")
                project = item.get("project")
                chain = item.get("chain")
                apr = float(item.get("apy", 0))

                if apr > 0 and symbol:
                    out.append({
                        "source": f"{project} ({chain})",
                        "asset": symbol.upper(),
                        "apr": apr,
                        "type": "DeFi",
                        "timestamp": datetime.utcnow()
                    })
        else:
            print("DefiLlama resp:", resp.status_code, resp.text)
    except Exception as e:
        print("DefiLlama error:", e)
    return out

def get_lido_eth_apr():
    """
    Прямой APR от Lido (ETH стейкинг)
    """
    out = []
    try:
        url = "https://stake.lido.fi/api/steth-apr"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            apr = float(resp.json())
            out.append({
                "source": "Lido",
                "asset": "ETH",
                "apr": apr * 100,   # в проценты
                "type": "DeFi",
                "timestamp": datetime.utcnow()
            })
        else:
            print("Lido resp:", resp.status_code, resp.text)
    except Exception as e:
        print("Lido error:", e)
    return out
