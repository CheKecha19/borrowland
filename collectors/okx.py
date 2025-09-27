# collectors/okx.py
from datetime import datetime
from config import OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSPHRASE
from collectors.utils import okx_get

def get_okx_borrow_rates():
    out = []
    try:
        resp = okx_get("/api/v5/finance/savings/lending-rate-summary",
                       OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSPHRASE)
        data = resp.json()
        for item in data.get("data", []):
            asset = item.get("ccy")
            apr = float(item.get("avgLoanRate", 0)) * 100
            out.append({"exchange": "OKX", "asset": asset.upper(), "apr": apr, "timestamp": datetime.utcnow()})
    except Exception as e:
        print("OKX borrow error:", e)
    return out

def get_okx_staking_rates():
    out = []
    try:
        resp = okx_get("/api/v5/finance/staking-defi/offers",
                       OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSPHRASE)
        data = resp.json()
        for item in data.get("data", []):
            asset = item.get("ccy")
            apr = float(item.get("apy", 0)) * 100
            out.append({"source": "OKX Earn", "asset": asset.upper(), "apr": apr, "type": "CeFi", "timestamp": datetime.utcnow()})
    except Exception as e:
        print("OKX staking error:", e)
    return out
