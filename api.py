from fastapi import FastAPI
import redis

app = FastAPI()
client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API des transactions"}

@app.get("/transactions/")
def get_transactions():
    transaction_ids = client.lrange("transactions_list", 0, -1)
    transactions = []
    for tid in transaction_ids:
        transaction_data = client.hgetall(f"transaction:{tid.decode()}")
        transactions.append({k.decode(): v.decode() for k, v in transaction_data.items()})
    return transactions
