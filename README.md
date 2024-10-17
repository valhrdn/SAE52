```markdown
# Collecte de Logs avec Docker

## Objectif

Ce projet met en œuvre une solution simple de collecte de logs via Docker. L'objectif est de collecter les logs d'un système ou d'une application et de les afficher ou les transmettre pour analyse. Cette solution est basée sur un conteneur Docker qui surveille et collecte les logs, ce qui permet de visualiser en temps réel les informations liées à l'utilisation du CPU, de la RAM et du disque, ainsi que d'autres métriques pertinentes.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker** : [Installer Docker](https://docs.docker.com/get-docker/)
- **InfluxDB** (si vous souhaitez stocker les logs dans une base de données)
- **Grafana** (optionnel, pour la visualisation des logs)

## Étapes de Configuration

### 1. Création du `Dockerfile`

Voici un `Dockerfile` simple qui met en place une application Python pour la collecte de logs système :

```dockerfile
# Utiliser une image de base Python
FROM python:3.10-slim

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install psutil influxdb-client

# Créer un répertoire de travail
WORKDIR /app

# Copier les scripts dans le conteneur
COPY monitor.py /app/monitor.py

# Exposer le port 5000 pour une application web ou autre
EXPOSE 5000

# Commande par défaut pour lancer le script de monitoring
CMD ["python", "monitor.py"]
```

Ce fichier Docker :

1. Utilise une image Python 3.10 comme base.
2. Installe les dépendances nécessaires pour la collecte de logs (comme `psutil` pour surveiller l'utilisation des ressources et `influxdb-client` pour l'envoi des données).
3. Définit un point d'entrée pour exécuter le script Python qui surveille le système.

### 2. Création du script `monitor.py`

Voici un exemple de script Python qui collecte les logs système (CPU, RAM, Disque) et les envoie à une base de données InfluxDB :

```python
import psutil
import time
from influxdb_client import InfluxDBClient, WriteOptions

# Configuration de la connexion à InfluxDB
token = "votre_token_influxdb"
org = "votre_org"
bucket = "monitoring_data"

# Initialisation du client InfluxDB
client = InfluxDBClient(url="http://localhost:8086", token=token)

# Fonction pour surveiller les ressources système
def monitor_system():
    write_api = client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=1000))
    
    while True:
        # Collecte des métriques
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        # Création d'un point de données pour InfluxDB
        data_point = {
            "measurement": "system_usage",
            "tags": {"host": "docker-container"},
            "fields": {
                "cpu_usage": cpu,
                "ram_usage": ram,
                "disk_usage": disk
            }
        }
        
        # Envoi des données à InfluxDB
        write_api.write(bucket=bucket, org=org, record=data_point)
        time.sleep(5)

# Lancer la surveillance
if __name__ == "__main__":
    monitor_system()
```

### 3. Construction et Lancement du Conteneur

Pour construire l'image Docker, exécutez la commande suivante à partir du répertoire contenant le fichier `Dockerfile` :

```bash
docker build -t log-monitor .
```

Ensuite, lancez le conteneur :

```bash
docker run -d --name=log-container log-monitor
```

Cela démarre un conteneur qui exécute le script Python, collectant des logs système en temps réel et les envoyant à une base InfluxDB.

### 4. Visualisation des Logs

Pour visualiser les logs, vous pouvez utiliser une solution comme Grafana. Voici les étapes pour configurer Grafana afin de récupérer et afficher les données stockées dans InfluxDB :

1. Connectez-vous à l'interface Grafana.
2. Ajoutez une source de données InfluxDB en spécifiant l'URL `http://localhost:8086` et en utilisant le bucket, le token et l'organisation définis dans le script Python.
3. Créez un tableau de bord pour visualiser les métriques comme l'utilisation du CPU, de la RAM et du disque.

## Gestion des Conteneurs

### Arrêter un conteneur

Pour arrêter le conteneur, utilisez :

```bash
docker stop log-container
```

### Supprimer un conteneur

Pour supprimer le conteneur après l'avoir arrêté :

```bash
docker rm log-container
```

### Redémarrer le conteneur

Si vous devez redémarrer le conteneur après l'avoir modifié ou arrêté :

```bash
docker run -d --name=log-container log-monitor
```

### Consulter les logs du conteneur

Vous pouvez consulter les logs générés par le conteneur Docker avec la commande suivante :

```bash
docker logs log-container
```

## Conclusion

Ce projet met en œuvre une solution simple et efficace pour la collecte de logs système en utilisant Docker. Les logs sont envoyés à une base de données InfluxDB et peuvent être visualisés à l'aide de Grafana ou d'autres outils de monitoring. La simplicité de cette solution permet une prise en main rapide et une extension facile pour surveiller d'autres aspects du système.
```

Cela couvre la création du `Dockerfile`, l'installation des dépendances, la collecte de logs avec `monitor.py`, et les étapes pour construire et lancer le conteneur Docker pour une surveillance simple des logs.
