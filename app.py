app.py – KHMScanner par KHMMarketing

========== 1. IMPORTS ET CONFIGURATION ==========

import streamlit as st import pandas as pd import numpy as np import datetime import plotly.graph_objects as go from binance.client import Client import smtplib from email.mime.text import MIMEText from email.mime.multipart import MIMEMultipart from twilio.rest import Client as TwilioClient import time

Configuration Binance (clé à remplacer par les tiennes)

API_KEY = "TON_API_KEY" API_SECRET = "TON_API_SECRET" client = Client(API_KEY, API_SECRET)

Configuration email (pour alerte)

EMAIL_SENDER = "ton.email@gmail.com" EMAIL_PASSWORD = "ton_mot_de_passe_app" EMAIL_RECEIVER = "destinataire@email.com"

Configuration Twilio (alerte SMS)

TWILIO_SID = "TON_TWILIO_SID" TWILIO_TOKEN = "TON_TWILIO_TOKEN" TWILIO_FROM = "+11234567890" TWILIO_TO = "+689XXXXXXXX"

Streamlit UI

st.set_page_config(page_title="KHMScanner", layout="wide") st.title("Scanner de Marché – KHMScanner")

========== 2. FONCTIONS UTILES ==========

def get_klines(symbol, interval, limit): klines = client.get_klines(symbol=symbol, interval=interval, limit=limit) df = pd.DataFrame(klines, columns=[ 'timestamp', 'open', 'high', 'low', 'close', 'volume', '', '', '', '', '', '' ]) df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float) return df[['timestamp', 'open', 'high', 'low', 'close']]

def detect_support_resistance(df): supports, resistances = [], [] for i in range(2, len(df) - 2): if df['low'][i] < df['low'][i-1] and df['low'][i] < df['low'][i+1]: supports.append((df['timestamp'][i], df['low'][i])) if df['high'][i] > df['high'][i-1] and df['high'][i] > df['high'][i+1]: resistances.append((df['timestamp'][i], df['high'][i])) return supports, resistances

def send_email_alert(subject, body): msg = MIMEMultipart() msg['From'] = EMAIL_SENDER msg['To'] = EMAIL_RECEIVER msg['Subject'] = subject msg.attach(MIMEText(body, 'plain')) server = smtplib.SMTP('smtp.gmail.com', 587) server.starttls() server.login(EMAIL_SENDER, EMAIL_PASSWORD) server.send_message(msg) server.quit()

def send_sms_alert(body): client_sms = TwilioClient(TWILIO_SID, TWILIO_TOKEN) client_sms.messages.create( body=body, from_=TWILIO_FROM, to=TWILIO_TO )

========== 3. SCANNER EN TEMPS RÉEL ==========

def run_scanner(): symbol = st.sidebar.text_input("Symbole de trading", "BTCUSDT") interval = st.sidebar.selectbox("Intervalle", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3) limit = st.sidebar.slider("Nombre de bougies", 50, 500, 100)

df = get_klines(symbol, interval, limit)
supports, resistances = detect_support_resistance(df)

fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Bougies'
))
for s in supports:
    fig.add_hline(y=s[1], line_dash="dot", line_color="green")
for r in resistances:
    fig.add_hline(y=r[1], line_dash="dash", line_color="red")

st.plotly_chart(fig, use_container_width=True)

if supports:
    dernier_support = supports[-1][1]
    if df['close'].iloc[-1] > dernier_support:
        send_email_alert("Achat potentiel détecté", f"Le prix a franchi le support à {dernier_support}")
        send_sms_alert(f"[KHMScanner] Achat potentiel sur {symbol} à {dernier_support}")

if resistances:
    derniere_resistance = resistances[-1][1]
    if df['close'].iloc[-1] < derniere_resistance:
        send_email_alert("Vente potentielle détectée", f"Le prix a chuté sous la résistance à {derniere_resistance}")
        send_sms_alert(f"[KHMScanner] Vente potentielle sur {symbol} à {derniere_resistance}")

========== 4. LANCEMENT ==========

if st.button("Lancer le scanner"): run_scanner()

Pied de page

st.markdown("""

Développé avec amour par [KHMMarketing] """)

