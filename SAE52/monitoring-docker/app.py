from flask import Flask, jsonify, send_from_directory
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # Serve the index.html file


@app.route('/logs')
def get_logs():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return jsonify({
        "cpu_usage": cpu,
        "ram_usage": ram,
        "disk_usage": disk
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Expose port 5000

