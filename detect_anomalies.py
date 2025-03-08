import pandas as pd
from sklearn.ensemble import IsolationForest
import redis

# Connexion à Redis
client = redis.Redis(host='localhost', port=6379, db=0)

def detect_anomalies():
    print("Récupération des transactions depuis Redis...")
    transaction_ids = client.lrange("transactions_list", 0, -1)
    transactions = []

    if not transaction_ids:
        print("Aucune transaction trouvée dans Redis.")
        return

    for tid in transaction_ids:
        transaction_data = client.hgetall(f"transaction:{tid.decode()}")

        try:
            transactions.append({
                k.decode(): float(v.decode()) if k.decode() == "amount" else v.decode()
                for k, v in transaction_data.items()
            })
        except Exception as e:
            print(f"Erreur de traitement de la transaction {tid.decode()}: {e}")

    # Vérification si des transactions ont été chargées
    if not transactions:
        print("Aucune transaction valide n'a été chargée.")
        return

    # Création du DataFrame
    df = pd.DataFrame(transactions)

    # Vérification si la colonne 'amount' est bien présente
    if 'amount' not in df.columns:
        print("Erreur : La colonne 'amount' est absente du DataFrame.")
        return

    # Vérification des types
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.dropna(subset=['amount'], inplace=True)  # Supprimer les lignes avec valeurs NaN dans 'amount'

    print(f"{len(df)} transactions chargées pour analyse.")

    # Détection des anomalies avec Isolation Forest
    print("Détection des anomalies en cours...")
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[['amount']])

    anomalies_detected = df[df['anomaly_score'] == -1]

    for _, row in anomalies_detected.iterrows():
        client.sadd("anomalies", row['transaction_id'])

    print(f"Détection d'anomalies terminée. {len(anomalies_detected)} anomalies détectées.")

if __name__ == "__main__":
    detect_anomalies()
