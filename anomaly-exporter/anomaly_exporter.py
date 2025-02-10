from flask import Flask, request, jsonify, Response
import time
import threading
from collections import deque, defaultdict

# Créer l'application Flask
app = Flask(__name__)

# Stockage des métriques avec leur timestamp, limité à 30 éléments
metrics_data = deque(maxlen=30)

anomaly_counters = defaultdict(int)

# Route pour recevoir les données POST et stocker la métrique avec timestamp
@app.route('/update-metric', methods=['POST'])
def update_metric():
    try:
        data = request.json
        metric_type = data.get('type')
        metric_value = data.get('metric_value')
        timestamp = int(data.get('timestamp', time.time())) *1000

        print(f"Received data: {data}")

        if metric_type and metric_value is not None:
            # Ajouter la nouvelle métrique à la deque
            # Vérifier si la métrique existe déjà
            for m_type, m_value, m_timestamp in metrics_data:
                if m_type == metric_type and m_timestamp == timestamp:
                    return jsonify({"status": "error", "message": "Duplicate metric"}), 400
            
            anomaly_counters[metric_type] += 1
            # Ajouter la nouvelle métrique à la deque
            metrics_data.append((metric_type, metric_value, timestamp))
            return jsonify({"status": "success", "message": "Metric updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Missing parameters"}), 400
    except Exception as e:
        print(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

# Route pour exposer les métriques dans un format compatible Prometheus
@app.route('/metrics')
def metrics():
    response = "# HELP metric_value Valeur de la métrique du container avec timestamp\n"
    response += "# TYPE metric_value gauge\n"

    for metric_type, metric_value, timestamp in metrics_data:
        response += f'anomaly{{type="{metric_type}"}} {metric_value} {timestamp}\n'

    response += "# HELP anomaly_counter Nombre d'anomalies détectées par type\n"
    response += "# TYPE anomaly_counter counter\n"

    for metric_type, count in anomaly_counters.items():
        response += f'anomaly_counter{{type="{metric_type}"}} {count}\n'

    return Response(response, mimetype="text/plain")

# Démarrer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Serveur Flask sur le port 12345