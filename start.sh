docker compose down -v
cd ml-anomaly-detection
mvn clean package
cd ..
docker compose up -d --build
docker exec -it anomaly-detection-supervisor-1 "sh" "/storm/supervisor/setup.sh"