from flask import Flask
from prometheus_client import start_http_server, Gauge
import csv
import time

app = Flask(__name__)

# Define a Prometheus Gauge metric
metric_gauge = Gauge('metric_value', 'Description of metric_value')

def read_csv_and_update_metrics():
    with open('sample_data/metrics.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            timestamp = row['timestamp']
            metric_value = float(row['metric_value'])
            metric_gauge.set(metric_value)
            time.sleep(1)  # Simulate real-time data

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    start_http_server(8000)  # Start Prometheus metrics server on port 8000
    read_csv_and_update_metrics()
    app.run(host='0.0.0.0', port=9799)