import pandas as pd
from adtk.detector import LevelShiftAD
from adtk.data import validate_series
import matplotlib.pyplot as plt

# Charger les données CSV
def load_data(csv_file):
    df = pd.read_csv(csv_file, parse_dates=["timestamp"], index_col="timestamp")
    return df

# Détection d'anomalies avec LevelShiftAD
def detect_anomalies(df):
    df = validate_series(df)  # Validation du format
    level_shift_ad = LevelShiftAD(window=10, c=3.0)  # Création du modèle avec une fenêtre de 10 valeurs et seuil de 3.0
    anomalies = level_shift_ad.fit_detect(df)
    return anomalies

# Afficher les résultats
def plot_results(df, anomalies):
    plt.figure(figsize=(12, 6))
    plt.plot(df, label="Metric Value", color='blue')
    plt.scatter(anomalies.index, df[anomalies], color='red', label="Anomalies", marker='x')
    plt.legend()
    plt.title("Anomaly Detection using LevelShiftAD")
    plt.show()

if __name__ == "__main__":
    csv_file = "test.csv"  # Remplace par le chemin réel du fichier CSV
    df = load_data(csv_file)
    anomalies = detect_anomalies(df)
    plot_results(df, anomalies)
