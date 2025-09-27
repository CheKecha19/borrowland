# collectors/binance.py
import requests
from datetime import datetime
from config import BINANCE_API_KEY, BINANCE_API_SECRET

BASE = "https://api.binance.com"

def get_binance_borrow_rates():
    """
    Пример (упрощённый). Binance имеет разные endpoints — для production нужно использовать авторизацию.
    Возвращает список словарей: {exchange, asset, apr, timestamp}
    """
    # NOTE: реальное получение borrow-rate требует авторизации и проверки документации Binance.
    # Здесь мы пробуем public endpoint для маржинальных пар как демонстрацию — заменяй на реальную реализацию.
    out = []
    try:
        # Технически это не реальный borrow APR endpoint — см. доки Binance.
        resp = requests.get(f"{BASE}/sapi/v1/margin/loan")
        if resp.status_code == 200:
            data = resp.json()
            # адаптация к формату ответа
            for item in data:
                asset = item.get("asset")
                # demo: нет реального APR в этом ответе — оставим placeholder 0
                out.append({"exchange": "Binance", "asset": asset, "apr": 0.0, "timestamp": datetime.utcnow()})
    except Exception as e:
        # логирование (print для простоты)
        print("Binance borrow error:", e)
    return out

def get_binance_staking_rates():
    """
    Возврат APR для staking / locked products. Лучше использовать Binance Earn API с ключами.
    Возвращает: {source, asset, apr, type, timestamp}
    """
    out = []
    try:
        # Simplified: Binance имеет эндпоинты для 'savings'/'staking' — проверяй доки и используй подписанные запросы
        resp = requests.get(f"{BASE}/sapi/v1/lending/project/list")  # примерный endpoint, нужен ключ
        if resp.status_code == 200:
            data = resp.json()
            # Приведи data к формату
            for item in data:
                asset = item.get("asset")
                # placeholder APR:
                apr = float(item.get("annualInterestRate", 0)) if item.get("annualInterestRate") else 0.0
                out.append({"source": "Binance Earn", "asset": asset, "apr": apr*100 if apr<10 else apr, "type":"CeFi", "timestamp": datetime.utcnow()})
    except Exception as e:
        print("Binance staking error:", e)
    return out
