from celery import Celery
import os

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def detect_anomalies_task():
    os.system("python detect_anomalies.py")
    return "Détection des anomalies exécutée avec succès"

if __name__ == "__main__":
    detect_anomalies_task()
