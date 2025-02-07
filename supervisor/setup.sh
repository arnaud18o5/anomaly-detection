#!/bin/bash
storm supervisor

# Mettre à jour les paquets et installer Python et pip
apt-get update && apt-get install -y python3 python3-pip python3-venv

# Créer un environnement virtuel
python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les dépendances Python
/opt/venv/bin/pip install --no-cache-dir -r /storm/supervisor/requirements.txt

# Définir les variables d'environnement pour utiliser l'environnement virtuel
echo 'export PATH="/opt/venv/bin:$PATH"' >> /etc/profile

storm jar /storm/ml-anomaly-detection-1.0-SNAPSHOT.jar org.anomalydetection.AnomalyDetectionTopology