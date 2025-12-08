# src/evaluate.py
import shutil
import os
import csv
from src.pipeline import run_text_pipeline
from src.verify_logs import verify_logs

ARTIFACT_DIR = "/app/artifacts/release"
LOG_PATH = os.getenv("LOG_CSV_PATH", "/app/data/output/logs.csv")

def _reset_logs():
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

def scenario_clean():
    _reset_logs()
    run_text_pipeline("hello world", "sha256")
    result = verify_logs()
    return {"scenario": "clean", **result}

def scenario_tampered_sig():
    _reset_logs()
    run_text_pipeline("tamper me", "sha256")
    # manually corrupt signature in last row
    rows = []
    with open(LOG_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    rows[-1]["sig"] = "00" + rows[-1]["sig"][2:]
    with open(LOG_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    result = verify_logs()
    return {"scenario": "tampered_sig", **result}

def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    results = [scenario_clean(), scenario_tampered_sig()]
    out_csv = os.path.join(ARTIFACT_DIR, "eval_metrics.csv")
    with open(out_csv, "w", newline="") as f:
        fieldnames = ["scenario", "total_records",
                      "invalid_signatures", "sequence_gaps", "status"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in fieldnames})

if __name__ == "__main__":
    main()
