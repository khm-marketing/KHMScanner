# KHMScanner : Le Radar Crypto de l'élite - by KHMMarketing

import streamlit as st
import pandas as pd
import ccxt
import numpy as np
import time

st.set_page_config(page_title="KHMScanner", layout="wide")
st.title("KHMScanner - Scanner Crypto Intelligent")

# Initialisation de l'exchange (Binance)
binance = ccxt.binance()

# Récupérer les paires disponibles
@st.cache_data(ttl=3600)
def get_all_symbols():
    markets = binance.load_markets()
    symbols = [symbol for symbol in markets if symbol.endswith('/USDT') and ':' not in symbol]
    return sorted(symbols)

# Détection automatique des supports et résistances
@st.cache_data(ttl=300)
def detect_sr(levels):
    supports = []
    resistances = []
    for i in range(2, len(levels)-2):
        if levels[i] < levels[i-1] and levels[i] < levels[i+1] and levels[i+1] < levels[i+2]:
            supports.append((i, levels[i]))
        elif levels[i] > levels[i-1] and levels[i] > levels[i+1] and levels[i+1] > levels[i+2]:
            resistances.append((i, levels[i]))
    return supports, resistances

# Récupération des données OHLCV
@st.cache_data(ttl=300)
def get_ohlcv(symbol, timeframe='1h', limit=100):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        st.warning(f"Erreur sur {symbol} : {e}")
        return None

# Analyse d’une crypto
def analyze_symbol(symbol):
    df = get_ohlcv(symbol)
    if df is not None:
        close_prices = df['close'].values
        supports, resistances = detect_sr(close_prices)

        current_price = close_prices[-1]
        last_support = supports[-1][1] if supports else 'N/A'
        last_resistance = resistances[-1][1] if resistances else 'N/A'

        with st.expander(f"Analyse de {symbol}", expanded=False):
            st.metric(label="Prix actuel", value=f"{current_price:.4f}")
            st.metric(label="Dernier support", value=last_support)
            st.metric(label="Dernière résistance", value=last_resistance)
            st.line_chart(df.set_index('timestamp')['close'])
        return (symbol, current_price, last_support, last_resistance)
    return None

# Interface utilisateur
st.sidebar.title("Options du Scanner")
symbols = get_all_symbols()
selected_symbols = st.sidebar.multiselect("Choisis tes cryptos (max 5)", symbols, default=symbols[:5])

results = []
progress_bar = st.sidebar.progress(0)

for i, symbol in enumerate(selected_symbols):
    result = analyze_symbol(symbol)
    if result:
        results.append(result)
    progress_bar.progress((i + 1) / len(selected_symbols))

# Résumé global
if results:
    st.header("Récapitulatif Global")
    summary_df = pd.DataFrame(results, columns=["Symbole", "Prix actuel", "Support", "Résistance"])
    st.dataframe(summary_df)
else:
    st.info("Aucune donnée à afficher pour le moment.")

# Footer
st.markdown("""
---
KHMScanner propulsé par **KHMMarketing** | Données fournies par Binance | Interface Streamlit
""")
