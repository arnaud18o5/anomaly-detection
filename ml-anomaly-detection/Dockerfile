# Utiliser une image de base Storm
FROM storm

# Installer Python et pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Créer un environnement virtuel
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les dépendances Python
COPY ./requirements.txt /tmp/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Définir les variables d'environnement pour utiliser l'environnement virtuel
ENV PATH="/opt/venv/bin:$PATH"

# Définir le point d'entrée pour exécuter le Supervisor
ENTRYPOINT ["storm", "supervisor"]