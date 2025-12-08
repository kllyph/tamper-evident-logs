import csv
import json
import os
import hmac
import hashlib
from datetime import datetime

LOG_PATH = os.getenv("LOG_CSV_PATH", "/app/artifacts/release/logs.csv")
OUT_PATH = "/app/artifacts/release/verification_results.json"

SECRET_KEY = b"supersecretkey"  # must match logging.py


def compute_signature(record: dict) -> str:
    """Recompute HMAC signature for a base record."""
    base = {k: v for k, v in record.items() if k != "sig"}
    
    payload = json.dumps(base, sort_keys=True).encode()
    return hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()


def verify_logs():
    total = 0
    invalid = 0
    sequence_gaps = 0

    last_seq = -1
    tampered_rows = []

    with open(LOG_PATH, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1

            # Detect missing or unordered sequence numbers
            seq = int(row.get("seq", total - 1))
            if seq != last_seq + 1:
                sequence_gaps += 1
            last_seq = seq

            # Recompute signature
            computed = compute_signature(row)
            if computed != row["sig"]:
                invalid += 1
                tampered_rows.append(seq)

    status = "OK"
