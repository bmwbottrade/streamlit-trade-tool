import streamlit as st
import requests
import time
import hmac
import hashlib
import base64
import datetime

# ✅ Secrets
API_KEY = st.secrets["BITGET_API_KEY"]
SECRET_KEY = st.secrets["BITGET_SECRET_KEY"]
PASSPHRASE = st.secrets["BITGET_PASSPHRASE"]

BASE_URL = "https://api.bitget.com/api/v2"

# 🔐 Signature 생성 함수
def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    mac = hmac.new(bytes(secret, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod=hashlib.sha256)
    d = mac.digest()
    return base64.b64encode(d).decode()

def get_timestamp():
    return datetime.datetime.utcnow().isoformat("T", "milliseconds") + "Z"

# 📡 공통 요청 함수
def send_request(method, path, params=None):
    timestamp = get_timestamp()
    body = "" if not params else json.dumps(params)
    sign = generate_signature(SECRET_KEY, timestamp, method, path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }
    url = BASE_URL + path
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, json=params)
        return response.json()
    except Exception as e:
        print("[Error] API request failed:", e)
        return {}

# 💰 자산 조회 함수 (에러 처리 포함)
def get_balance():
    try:
        endpoint = "/account/accountList"
        res = send_request("GET", endpoint)
        if res and "data" in res:
            assets = res["data"]
            usdt = next((item for item in assets if item.get("marginCoin") == "USDT"), None)
            if usdt:
                return float(usdt.get("available", 0.0))
        return 0.0
    except Exception as e:
        print("Balance fetch error:", e)
        return 0.0

# 📈 현재가 조회 함수
def get_top_price():
    try:
        endpoint = "/mix/market/tickers"
        res = send_request("GET", endpoint)
        if res and "data" in res:
            return float(res["data"][0]["lastPr"])
        return None
    except Exception as e:
        print("Price fetch error:", e)
        return None

# 🌐 Streamlit 화면
st.title("✅ Bitget API 테스트")

balance = get_balance()
price = get_top_price()

st.metric("USDT 자산", f"{balance:,.2f} USDT")
st.metric("선물 현재가", f"{price:,.4f}" if price else "조회 실패")
