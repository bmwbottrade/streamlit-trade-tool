import streamlit as st

st.set_page_config(page_title="Bitget Manual Trading UI", layout="wide")

st.title("📈 Bitget 수동 지정가 매매 도구")

# 종목 선택
symbol = st.selectbox("📌 종목 선택 (Top 10 거래량)", ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT", "TRXUSDT", "LTCUSDT"])

# 현재가 조회
current_price = st.number_input("💰 현재가", value=65000.0, format="%.2f")

# 진입가 수동 설정 or 현재가 진입 선택
entry_method = st.radio("진입 방식 선택", ["현재가 기준", "직접 입력"])
entry_price = current_price if entry_method == "현재가 기준" else st.number_input("🟢 진입가 입력", value=current_price, format="%.2f")

# 손절가, 익절가 입력
stop_loss_price = st.number_input("🔴 손절가 (시장가 청산)", value=entry_price * 0.99, format="%.2f")
take_profit_price = st.number_input("🟢 익절가 (지정가)", value=entry_price * 1.02, format="%.2f")

# 자본금, 최대 손실 비율 입력
capital = st.number_input("💼 자본금 (USDT)", value=1000.0, step=100.0)
max_loss_pct = st.slider("🚨 최대 손실 허용 비율 (%)", min_value=0.1, max_value=5.0, value=1.0)

# 주문 수량 자동 계산
loss_amount = capital * (max_loss_pct / 100)
quantity = round(loss_amount / abs(entry_price - stop_loss_price), 3)

# 결과 요약
st.write("📊 계산된 주문 수량:", quantity)

# 버튼
col1, col2 = st.columns(2)
if col1.button("📥 지정가 매수"):
    st.success(f"{symbol} - 지정가 매수 주문 (진입가: {entry_price}, 수량: {quantity}) 전송됨")

if col2.button("📤 지정가 매도"):
    st.success(f"{symbol} - 지정가 매도 주문 (진입가: {entry_price}, 수량: {quantity}) 전송됨")
