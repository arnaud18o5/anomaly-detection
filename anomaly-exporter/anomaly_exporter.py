from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Gauge
import time
import threading

# Créer l'application Flask
app = Flask(__name__)

# Déclaration de la métrique
metric_gauge = Gauge('metric_value', 'Valeur de la métrique du container', ['type'])


# Route pour recevoir les données POST et mettre à jour la métrique
@app.route('/update-metric', methods=['POST'])
def update_metric():
    try:
        # Récupérer les données de la requête
        data = request.json
        type = data.get('type')
        metric_value = data.get('metric_value')
        print(f"Received data: {data}")

        # Mettre à jour la métrique
        if type and metric_value is not None:
            metric_gauge.labels(type=type).set(metric_value)
            return jsonify({"status": "success", "message": "Metric updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Missing parameters"}), 400
    except Exception as e:
        print(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    

# Démarrer le serveur HTTP pour exposer les métriques à Prometheus
if __name__ == '__main__':
    expiration_time = 10  # Durée d'expiration des métriques en secondes
    start_http_server(1234)  # Prometheus scrutera ce port
    app.run(host='0.0.0.0', port=12345)  # Serveur Flask sur le port 5000
