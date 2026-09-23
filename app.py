import datetime
import pandas as pd
import streamlit as st
import yfinance as yf

# 設定網頁頁面
st.set_page_config(
    page_title="台股與國際資產儀表板", page_icon="📈", layout="centered"
)

st.title("🌍 國際資產與台股監控儀表板")
st.caption(
    f"最後更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

if st.button("🔄 刷新最新市場數據"):
    st.rerun()

# 1. 抓取匯率與黃金
st.subheader("📊 國際資產現況")
col1, col2 = st.columns(2)

try:
    usdtwd_hist = yf.Ticker("TWD=X").history(period="2d")["Close"]
    usdtwd = usdtwd_hist.iloc[-1]
    usdtwd_chg = ((usdtwd - usdtwd_hist.iloc[-2]) / usdtwd_hist.iloc[-2]) * 100
    col1.metric("💵 美元 / 台幣", f"{round(usdtwd, 2)} 元", f"{round(usdtwd_chg, 2)}%")
except Exception:
    col1.metric("💵 美元 / 台幣", "無法取得")

try:
    gold_usd = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
    gold_twd_g = round((gold_usd * usdtwd) / 31.1035, 1)
    buy_gold = round(gold_twd_g * 0.96, 1)
    col2.metric(
        "🪙 國際黃金 (台幣/g)", f"{gold_twd_g} 元", f"建議: {buy_gold}元下"
    )
except Exception:
    col2.metric("🪙 國際黃金", "無法取得")

# 2. 核心股票卡片
st.subheader("📌 核心穩健關注標的")
CORE_STOCKS = {
    "2330.TW": {"name": "台積電", "buy_factor": 0.90, "sell_factor": 1.15},
    "2454.TW": {"name": "聯發科", "buy_factor": 0.88, "sell_factor": 1.12},
    "3653.TW": {"name": "健策", "buy_factor": 0.85, "sell_factor": 1.15},
    "3034.TW": {"name": "聯詠", "buy_factor": 0.92, "sell_factor": 1.10},
}

for ticker, config in CORE_STOCKS.items():
    try:
        hist = yf.Ticker(ticker).history(period="2d")["Close"]
        p = round(hist.iloc[-1], 1)
        prev = hist.iloc[-2]
        chg = round(((p - prev) / prev) * 100, 2)
        buy_p = round(p * config["buy_factor"], 1)
        sell_p = round(p * config["sell_factor"], 1)

        color_str = "#EF4444" if chg > 0 else "#22C55E"
        sign_str = "+" if chg > 0 else ""

        card_html = f"""
