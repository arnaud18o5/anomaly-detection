import time
import threading
import random
import csv
from flask import Flask
from prometheus_client import start_http_server, Gauge, Counter

app = Flask(__name__)

# Define a Prometheus Gauge metric
metric_gauge = Gauge('metric_value', 'Description of metric_value')
anomaly_counter = Counter('anomaly_counter', 'How many anomalies have been created')

def read_csv_and_update_metrics():
    while True:
        with open('sample_data/metrics.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                timestamp = row['timestamp']
                metric_value = float(row['metric_value'])
                gauss = 2
                if random.random() < 0.05:
                    anomaly_counter.inc()
                    gauss = 100
                offset = random.gauss(0, gauss)  # Gaussian distribution with mean 0 and standard deviation 5
                metric_gauge.set(metric_value + offset)
                time.sleep(1)  # Simulate real-time data


@app.route('/')
def trigger_absurd_metrics():
    return 'Metrics will be absurd for 5 seconds!'

if __name__ == '__main__':
    anomaly_counter.inc(0)  # Initialize the counter at 0
    start_http_server(8000)  # Start Prometheus metrics server on port 8000
    threading.Thread(target=read_csv_and_update_metrics).start()
    app.run(host='0.0.0.0', port=9799)