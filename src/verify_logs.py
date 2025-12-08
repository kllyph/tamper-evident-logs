import csv
import json
import os
import hmac
import hashlib
from datetime import datetime

# Use a relative default so it works both locally and in Docker
LOG_CSV_PATH = os.getenv("LOG_CSV_PATH", "data/output/logs.csv")
LOG_SECRET = os.getenv("LOG_SECRET", "dev-secret-key")
OUT_PATH = os.getenv(
    "VERIFY_JSON_PATH",
    "artifacts/release/verification_results.json",
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
    """
    Recompute the expected HMAC signature for a log row.

    We normalize everything to strings and use a deterministic JSON
    encoding (sort_keys=True) so logging and verification match exactly.
    """
    base = {k: str(row.get(k, "")) for k in HEADER_BASE_FIELDS}
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

            # Sequence check (optional, informational)
            try:
                seq = int(row.get("seq", total - 1))
            except (TypeError, ValueError):
                seq = total - 1

            if last_seq != -1 and seq != last_seq + 1:
                sequence_gaps += 1
            last_seq = seq

            # Signature check
            computed = _compute_sig(row)
            if computed != row["sig"]:
                invalid += 1
                tampered_rows.append(seq)

    # Treat invalid signatures as the primary failure signal
    status = "OK" if invalid == 0 else "FAIL"

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
