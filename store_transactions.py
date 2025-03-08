import redis
import pandas as pd

# Connexion à Redis via Homebrew (localhost)
client = redis.Redis(host='localhost', port=6379, db=0)

def store_transactions(csv_path):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        transaction_id = row['transaction_id']
        client.hset(f"transaction:{transaction_id}", mapping=row.to_dict())
        client.lpush("transactions_list", transaction_id)

    print("Transactions stockées avec succès.")

if __name__ == "__main__":
    store_transactions("data/transactions_data.csv")
