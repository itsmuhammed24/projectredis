import streamlit as st
import redis
import pandas as pd
import matplotlib.pyplot as plt

client = redis.Redis(host='localhost', port=6379, db=0)

st.title("Analyse des Transactions Bancaires")

def fetch_transactions():
    transaction_ids = client.lrange("transactions_list", 0, -1)
    transactions = []
    for tid in transaction_ids:
        transaction_data = client.hgetall(f"transaction:{tid.decode()}")
        transactions.append({k.decode(): v.decode() for k, v in transaction_data.items()})
    return pd.DataFrame(transactions)

df = fetch_transactions()
df['amount'] = df['amount'].astype(float)

st.write("Aperçu des transactions")
st.dataframe(df)

st.write("Répartition des montants")
plt.figure(figsize=(8, 6))
df['amount'].hist(bins=30, color='skyblue')
st.pyplot(plt)

st.write("Détection d'anomalies")
anomalies = client.smembers("anomalies")
st.write(f"Nombre d'anomalies détectées : {len(anomalies)}")
