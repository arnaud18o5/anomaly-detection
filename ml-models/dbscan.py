import sys
import json
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import DBSCAN

def detect_anomalies(data, eps=1, min_samples=2, window_size=10):
    """
    Applique DBSCAN sur une série temporelle pour détecter les anomalies en analysant les variations successives.
    
    :param data: Liste des valeurs de la série temporelle.
    :param eps: Seuil de regroupement pour DBSCAN.
    :param min_samples: Nombre minimal de points pour former un cluster.
    :param window_size: Taille de la fenêtre pour l'analyse.
    :return: Liste des indices où des anomalies sont détectées.
    """

    data = np.array(data)

    # 1️⃣ Fenêtres glissantes pour capturer les tendances locales
    # windows = np.array([data[i:i + window_size] for i in range(len(data) - window_size + 1)])
    # print("windows:" , windows)

    # # 2️⃣ Calcul des variations successives dans chaque fenêtre
    # diffs = np.diff(windows, axis=1)  # Diff entre chaque valeur successive

    # print(diffs)

    # 3️⃣ Normalisation des variations pour rendre DBSCAN robuste
    scaler = RobustScaler()
    diffs_scaled = scaler.fit_transform(data.reshape(-1,1))  # Reshape pour éviter les erreurs

    # 4️⃣ Application de DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(diffs_scaled)

    print(labels)

    # 5️⃣ Extraction des indices des anomalies (labels = -1)
    anomalies = np.where((labels == -1) | (labels == 1))[0]

    anomalies = [[bool(i in anomalies)] for i in range(len(data))]

    return json.dumps(anomalies)

if __name__ == "__main__":
    try:
        # Lire les données depuis les arguments JSON
        data = json.loads(sys.argv[1])
        result = detect_anomalies(data)
        print(result)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
