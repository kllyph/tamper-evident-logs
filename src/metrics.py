import json, os

METRICS_JSON_PATH = os.getenv("METRICS_JSON_PATH", "data/output/metrics.json")

def export_metrics(metrics: dict):
    os.makedirs(os.path.dirname(METRICS_JSON_PATH), exist_ok=True)
    with open(METRICS_JSON_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
