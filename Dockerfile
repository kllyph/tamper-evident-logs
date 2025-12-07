FROM python:3.11-slim

# Least privilege: create non-root user
RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/input/ ./data/input/

ENV PYTHONUNBUFFERED=1
ENV LOG_CSV_PATH=/app/data/output/logs.csv
ENV METRICS_JSON_PATH=/app/data/output/metrics.json
ENV LOG_SECRET=change-me

USER appuser
CMD ["python", "-m", "src.app"]
