import streamlit as st
import requests

st.set_page_config(page_title="Bitget 종목 실시간 확인", layout="wide")

st.title("📈 Bitget 종목 현재가 확인")

# Bitget API URL
BASE_URL = "https://api.bitget.com/api/v2"

# 상위 10개 종목 조회 함수
@st.cache_data(ttl=30)
def get_top_symbols():
    url = f"{BASE_URL}/mix/market/tickers?productType=umcbl"
    response = requests.get(url).json()
    if "data" in response:
        data = response["data"]
        sorted_data = sorted(data, key=lambda x: float(x.get("quoteVolume", 0)), reverse=True)
        return sorted_data[:10]
    return []

# 실시간 가격 정보 조회 함수
def get_symbol_info(symbol):
    url = f"{BASE_URL}/mix/market/ticker?symbol={symbol}"
    res = requests.get(url).json()
    if "data" in res:
        return res["data"]
    return {}

# 종목 선택
symbols = get_top_symbols()
symbol_names = [item["symbol"] for item in symbols]
selected_symbol = st.selectbox("📌 확인할 종목을 선택하세요", symbol_names)

# 선택된 종목의 실시간 정보 표시
if selected_symbol:
    info = get_symbol_info(selected_symbol)
    if info:
        st.subheader(f"✅ {selected_symbol} 실시간 정보")
        st.metric("현재가", f'{info["lastPr"]} USDT')
        st.metric("24시간 고가", f'{info["high24h"]} USDT')
        st.metric("24시간 저가", f'{info["low24h"]} USDT')
        st.metric("거래량", f'{info["baseVolume"]} {selected_symbol[:-6]}')
        st.metric("거래대금", f'{info["quoteVolume"]} USDT')
    else:
        st.error("⚠️ 종목 정보를 불러오는 데 실패했습니다.")
else:
    st.info("상위 거래량 기준 종목을 로딩 중입니다...")
