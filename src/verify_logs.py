# src/verify_logs.py
import csv
import json
import os
import hmac
import hashlib
from datetime import datetime

LOG_CSV_PATH = os.getenv("LOG_CSV_PATH", "/app/data/output/logs.csv")
LOG_SECRET = os.getenv("LOG_SECRET", "dev-secret-key")
OUT_PATH = os.getenv(
    "VERIFY_JSON_PATH",
    "/app/artifacts/release/verification_results.json",
)

HEADER_BASE_FIELDS = [
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
]

def _compute_sig(row: dict) -> str:
    base = {k: row.get(k, "") for k in HEADER_BASE_FIELDS}
    payload = json.dumps(base, sort_keys=True).encode()
    return hmac.new(LOG_SECRET.encode(), payload, hashlib.sha256).hexdigest()

def verify_logs() -> dict:
    total = 0
    invalid = 0
    sequence_gaps = 0
    tampered_rows = []

    last_seq = -1

    if not os.path.exists(LOG_CSV_PATH):
        raise FileNotFoundError(LOG_CSV_PATH)

    with open(LOG_CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1

            # sequence check
            seq = int(row["seq"])
            if seq != last_seq + 1:
                sequence_gaps += 1
            last_seq = seq

            # signature check
            computed = _compute_sig(row)
            if computed != row["sig"]:
                invalid += 1
                tampered_rows.append(seq)

    status = "OK" if invalid == 0 and sequence_gaps == 0 else "FAIL"

    result = {
        "file": LOG_CSV_PATH,
        "total_records": total,
        "invalid_signatures": invalid,
        "sequence_gaps": sequence_gaps,
        "tampered_rows": tampered_rows,
        "status": status,
        "verified_at": datetime.utcnow().isoformat() + "Z",
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    verify_logs()
