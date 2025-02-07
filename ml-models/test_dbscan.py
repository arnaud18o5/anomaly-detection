import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Charger les données CSV
def load_data(csv_file):
    df = pd.read_csv(csv_file, parse_dates=["timestamp"], index_col="timestamp")
    return df

# Détection d'anomalies avec DBSCAN
def detect_anomalies(df, eps=0.8, min_samples=3):
    data = df.values.reshape(-1, 1)
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)
    anomalies = df[labels == -1]
    return anomalies

# Afficher les résultats
def plot_results(df, anomalies):
    plt.figure(figsize=(12, 6))
    plt.plot(df, label="Metric Value", color='blue')
    plt.scatter(anomalies.index, anomalies, color='red', label="Anomalies", marker='x')
    plt.legend()
    plt.title("Anomaly Detection using DBSCAN")
    plt.show()

if __name__ == "__main__":
    csv_file = "test.csv"  # Remplace par le chemin réel du fichier CSV
    df = load_data(csv_file)
    anomalies = detect_anomalies(df)
    plot_results(df, anomalies)