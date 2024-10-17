import psutil  # Assurez-vous que cette ligne est présente
import time
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, WriteOptions

# Configuration de la connexion à InfluxDB
token = "fKcybJ2DCaIfuKdGWxQxt7RVrKPMQkMfsNAY3pPg3gc2PrTU98Bw7GJ8MK2GjDXHTAzRlaFhHsGKV2BSora6hg=="
org = "sae52"
bucket = "monitoring_data"

# Initialisation du client InfluxDB
client = InfluxDBClient(url="http://localhost:8086", token=token)

# Listes pour stocker les données
timestamps = []
cpu_usage = []
ram_usage = []
disk_usage = []

# Fonction pour surveiller les ressources système en temps réel
def monitor_system():
    write_api = client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=1000))

    while True:
        # Récupérer l'heure actuelle
        current_time = time.strftime("%H:%M:%S")

        # Récupérer l'usage du CPU, de la RAM et du disque
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # Ajouter les données dans les listes
        timestamps.append(current_time)
        cpu_usage.append(cpu)
        ram_usage.append(ram)
        disk_usage.append(disk)

        # Créer un point de données pour InfluxDB
        data_point = {
            "measurement": "system_usage",
            "tags": {"host": "macbook"},
            "fields": {
                "cpu_usage": cpu,
                "ram_usage": ram,
                "disk_usage": disk
            }
        }

        # Écrire les données dans InfluxDB
        write_api.write(bucket=bucket, org=org, record=data_point)

        # Afficher un graphique mis à jour
        plt.clf()
        plt.subplot(3, 1, 1)
        plt.plot(timestamps, cpu_usage, label="CPU Usage (%)")
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(timestamps, ram_usage, label="RAM Usage (%)", color='orange')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(timestamps, disk_usage, label="Disk Usage (%)", color='green')
        plt.legend()

        plt.pause(5)  # Pause de 5 secondes avant la mise à jour suivante

        # Limiter à 20 points pour éviter que le graphique ne devienne trop lourd
        if len(timestamps) > 20:
            timestamps.pop(0)
            cpu_usage.pop(0)
            ram_usage.pop(0)
            disk_usage.pop(0)

# Lancer la surveillance
if __name__ == "__main__":
    plt.ion()  # Mode interactif pour mettre à jour le graphique en continu
    monitor_system()

