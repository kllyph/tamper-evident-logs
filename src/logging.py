import csv, json, time, hmac, hashlib, os
from typing import Dict

LOG_CSV_PATH = os.getenv("LOG_CSV_PATH", "/app/data/output/logs.csv")
LOG_SECRET = os.getenv("LOG_SECRET", "dev-secret-key")

def _sign_record(record: Dict) -> str:
    msg = json.dumps(record, sort_keys=True).encode()
    return hmac.new(LOG_SECRET.encode(), msg, hashlib.sha256).hexdigest()

def append_log(event: str, details: Dict):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    base = {"timestamp": ts, "event": event, **details}
    signature = _sign_record(base)
    row = {**base, "sig": signature}
    os.makedirs(os.path.dirname(LOG_CSV_PATH), exist_ok=True)
    header = ["timestamp", "event"] + [k for k in details.keys()] + ["sig"]
    file_exists = os.path.exists(LOG_CSV_PATH)
    with open(LOG_CSV_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            w.writeheader()
        w.writerow(row)
