# Real-time Anomaly Detection System

This project implements a real-time anomaly detection system using Apache Storm for stream processing, Prometheus for metrics collection, and Grafana for visualization. The system monitors metrics in real-time and detects anomalies using machine learning models.

## Architecture

The system consists of several components:

- **Metrics Generator**: A Python application that generates and exposes metrics
- **Apache Storm**: Distributed real-time computation system
  - Nimbus: Storm master node
  - Supervisor: Worker nodes for processing
  - UI: Storm web interface
- **Prometheus**: Time-series database for metrics storage
- **Grafana**: Visualization platform for metrics and alerts
- **Anomaly Exporter**: Service that exports detected anomalies
- **Zookeeper**: Distributed coordination service for Storm

## Prerequisites

- Docker
- Docker Compose
- Java 8 or higher (for building Storm components)
- Maven (for building Java components)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/arnaud18o5/anomaly-detection.git
cd anomaly-detection
```

2. Build the Java components:

```bash
cd ml-anomaly-detection
mvn clean package
cd ..
```

3. Start the system using Docker Compose:

```bash
./start.sh
```

## Accessing the Services

- Grafana Dashboard: http://localhost:80
- Prometheus: http://localhost:9090
- Storm UI: http://localhost:8080
- Metrics Generator: http://localhost:8000
- Anomaly Exporter: http://localhost:12345

## Components Details

### Metrics Generator

- Generates and exposes metrics for monitoring
- Runs on port 9799 for metrics and 8000 for web interface

### Apache Storm

- Nimbus (Master): Runs on port 6627
- Supervisor: Processes the anomaly detection topology
- UI: Accessible on port 8080

### Prometheus

- Collects and stores metrics
- Configured with alertmanager for alerting
- Accessible on port 9090

### Grafana

- Visualizes metrics and anomalies
- Pre-configured dashboards and data sources
- Accessible on port 80

### Anomaly Exporter

- Exports detected anomalies
- Runs on ports 12345 and 1234

## Directory Structure

```
.
├── anomaly-exporter/     # Anomaly export service
├── grafana/             # Grafana configuration and dashboards
├── ml-anomaly-detection/ # Storm topology for anomaly detection
├── ml-models/           # Machine learning models
├── metrics-generator/   # Metrics generation service
├── prometheus/         # Prometheus configuration
├── supervisor/         # Storm supervisor configuration
└── ui/                # Storm UI configuration
```

## Monitoring and Alerts

The system uses Prometheus and Grafana for monitoring:

- Prometheus collects metrics from all components
- Grafana provides dashboards for visualization
- Alertmanager handles alert routing and notifications

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the terms of the license included in the repository.
