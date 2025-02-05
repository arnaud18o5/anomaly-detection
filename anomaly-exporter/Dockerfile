# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script Python et les fichiers nécessaires
COPY anomaly_exporter.py .

# Exposer le port sur lequel l'application écoute
EXPOSE 12345
EXPOSE 1234

# Définir le point d'entrée pour exécuter le script Python
ENTRYPOINT ["python", "anomaly_exporter.py"]