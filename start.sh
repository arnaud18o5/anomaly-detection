docker compose down -v
docker compose up -d --build
docker exec -it anomaly-detection-supervisor-1 "sh" "/storm/supervisor/setup.sh"