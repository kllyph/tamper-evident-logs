# src/logging.py
import csv, json, time, hmac, hashlib, os
from typing import Dict

LOG_CSV_PATH = os.getenv("LOG_CSV_PATH", "/app/data/output/logs.csv")
LOG_SECRET = os.getenv("LOG_SECRET", "dev-secret-key")

# simple in-process sequence counter
_SEQ = 0

HEADER = [
    "seq",
    "timestamp",
    "event",
    "source",
    "algo",
    "size",
    "path",
    "digest_prefix",
    "bytes",
    "items",
    "sig",
]

def _sign_record(record: Dict) -> str:
    msg = json.dumps(record, sort_keys=True).encode()
    return hmac.new(LOG_SECRET.encode(), msg, hashlib.sha256).hexdigest()

def append_log(event: str, details: Dict):
    global _SEQ
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    base = {
        "seq": _SEQ,
        "timestamp": ts,
        "event": event,
        "source": details.get("source", ""),
        "algo": details.get("algo", ""),
        "size": details.get("size", ""),
        "path": details.get("path", ""),
        "digest_prefix": details.get("digest_prefix", ""),
        "bytes": details.get("bytes", ""),
        "items": details.get("items", ""),
    }
    _SEQ += 1

    signature = _sign_record(base)
    row = {**base, "sig": signature}

    os.makedirs(os.path.dirname(LOG_CSV_PATH), exist_ok=True)
    file_exists = os.path.exists(LOG_CSV_PATH)
    with open(LOG_CSV_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if not file_exists:
            w.writeheader()
        w.writerow(row)
