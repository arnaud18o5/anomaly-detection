FROM python:3.9-slim

WORKDIR /app

COPY src/ /app/src
COPY sample_data/ /app/sample_data
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9799
EXPOSE 8000

CMD ["python", "src/app.py"]