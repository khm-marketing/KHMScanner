import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(page_title="KHMScanner", layout="wide")

# En-tête
st.title("KHMScanner - Scanner Crypto Automatisé")
st.markdown("""
Bienvenue sur **KHMScanner**, ton outil de détection automatique de :
- **Supports / résistances fréquents**
- **Tendances de marché**
- **Alertes achat / vente**
- Mise à jour automatique toutes les **minutes**
---
""")

# Zone d'information
st.info("Fonctionnalité complète bientôt disponible. Cette version est une base de travail. Déploiement progressif en cours.")

# Données simulées pour l'instant
data = {
    "Paire": ["BTC/USDT", "ETH/USDT", "BNB/USDT"],
    "Support détecté": [26500, 1750, 300],
    "Résistance détectée": [28000, 1900, 330],
    "Tendance": ["Haussière", "Neutre", "Baissière"],
    "Alerte": ["Achat possible", "Attente", "Vente possible"]
}
df = pd.DataFrame(data)

# Affichage du tableau
st.subheader("Analyse en temps réel (exemple)")
st.dataframe(df)

# Dernière mise à jour
st.caption(f"Dernière mise à jour : {dt.datetime.now().strftime('%
