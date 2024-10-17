# Utiliser l'image de base Python
FROM python:3.10-slim

# Mettre à jour le système et installer les dépendances
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install psutil influxdb-client matplotlib Flask

# Créer un répertoire de travail
WORKDIR /app

# Copier le script de surveillance dans le conteneur
COPY monitor.py .
# Copier le fichier HTML dans le conteneur
COPY index.html .
# Copier le script Flask dans le conteneur
COPY app.py .


# Exposer le port utilisé par Flask (5000)
EXPOSE 5000

# Commande par défaut pour exécuter le serveur Flask
CMD ["python", "app.py"]

