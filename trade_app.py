import streamlit as st
import requests
import time
import hmac
import hashlib
import base64
import datetime
import json

# 시크릿에서 키 불러오기
API_KEY = st.secrets["BITGET_API_KEY"]
SECRET_KEY = st.secrets["BITGET_SECRET_KEY"]
PASSPHRASE = st.secrets["BITGET_PASSPHRASE"]

BASE_URL = "https://api.bitget.com/api/v2"

# 시그니처 생성
def generate_signature(secret, timestamp, method, path, body=""):
    message = f"{timestamp}{method.upper()}{path}{body}"
    mac = hmac.new(bytes(secret, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()

# 타임스탬프 생성
def get_timestamp():
    return datetime.datetime.utcnow().isoformat("T", "milliseconds") + "Z"

# 공통 요청 함수
def send_request(method, path, params=None):
    timestamp = get_timestamp()
    body = json.dumps(params) if params else ""
    sign = generate_signature(SECRET_KEY, timestamp, method, path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = BASE_URL + path
    if method == "GET":
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, data=body)

    return response.json()

# 잔고 조회 (선물 USDT)
def get_balance():
    path = "/account/account/assets?productType=USDT-FUTURES"
    res = send_request("GET", path)
    assets = res.get("data", [])
    usdt = next((item for item in assets if item["marginCoin"] == "USDT"), None)
    return float(usdt["available"]) if usdt else None

# 현재가 조회 (예: BTCUSDT)
def get_last_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/mix/market/ticker?symbol={symbol}&productType=USDT-FUTURES"
    res = requests.get(url).json()
    return float(res["data"]["lastPr"]) if res.get("data") else None

# Streamlit UI
st.title("✅ Bitget API 테스트")

balance = get_balance()
price = get_last_price()

if balance is not None:
    st.success(f"API 연동 성공! 현재 USDT 잔고: {balance:.2f}")
else:
    st.error("❌ USDT 잔고 조회 실패 - API 확인 필요")

if price is not None:
    st.info(f"BTCUSDT 현재가: {price}")
else:
    st.warning("BTCUSDT 현재가 조회 실패")
