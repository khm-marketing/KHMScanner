import streamlit as st
import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="KHMScanner", layout="wide")

st.title("KHMScanner - Scanner Crypto Intelligent")

# Fonction pour récupérer les symboles disponibles
@st.cache_data
def get_all_symbols():
    try:
        binance = ccxt.binance()
        markets = binance.load_markets()
        return list(markets.keys())
    except Exception as e:
        st.error("Impossible de charger les marchés Binance. Vérifiez la connexion ou essayez plus tard.")
        st.stop()

# Fonction pour obtenir les données OHLCV
@st.cache_data
def get_ohlcv(symbol):
    try:
        binance = ccxt.binance()
        ohlcv = binance.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données pour {symbol}.")
        return None

# Barre latérale pour sélection
st.sidebar.title("Options du Scanner")
all_symbols = get_all_symbols()
symbols_to_display = st.sidebar.multiselect("Choisissez les cryptos à scanner :", all_symbols, default=["BTC/USDT", "ETH/USDT"])

# Affichage des graphiques
for symbol in symbols_to_display:
    df = get_ohlcv(symbol)
    if df is not None and not df.empty:
        support = df['low'].min()
        resistance = df['high'].max()

        st.subheader(f"{symbol}")
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )])
        fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support", annotation_position="bottom right")
        fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Résistance", annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Aucune donnée disponible pour {symbol}")
