# collectors/utils.py
import time
import hmac
import hashlib
import base64
import requests
import json

def okx_sign_request(method, path, body="", secret="", timestamp=None):
    ts = str(timestamp or time.time())
    message = ts + method.upper() + path + body
    mac = hmac.new(secret.encode(), message.encode(), hashlib.sha256)
    sign = base64.b64encode(mac.digest()).decode()
    return ts, sign

def okx_get(path, api_key, secret, passphrase="", params=None):
    body = "" if not params else json.dumps(params)
    ts, sign = okx_sign_request("GET", path, body, secret)
    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": sign,
        "OK-ACCESS-TIMESTAMP": ts,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }
    url = "https://www.okx.com" + path
    r = requests.get(url, headers=headers, params=params)
    return r

def bybit_get(path, params=None):
    url = "https://api.bybit.com" + path
    try:
        r = requests.get(url, params=params)
        return r
    except Exception as e:
        print("Bybit request error:", e)
        return None

def kucoin_get(path, params=None):
    url = "https://api.kucoin.com" + path
    try:
        r = requests.get(url, params=params)
        return r
    except Exception as e:
        print("KuCoin request error:", e)
        return None

def gate_get(path, params=None):
    url = "https://api.gateio.ws" + path
    try:
        r = requests.get(url, params=params)
        return r
    except Exception as e:
        print("Gate request error:", e)
        return None
