# Final Project: Combined Alpha–Beta Integrated Release

**Course:** CECS 478 (Sec. 01)

**Professor:** Samuel Addington

**Date:** 12/07/2025

**Authors:**

- Khoa Vu (030063200)
- Kelly Pham (03039600)

---

## Project Overview: Tamper-evident logs

Traditional logging systems are vulnerable once attackers gain elevated access—they can modify, delete, or reorder log entries with little evidence of tampering.
This project implements a full tamper-evident logging pipeline built on:
- Hash chaining
- HMAC-based signature verification
- Deterministic, reproducible logging format
- Evaluation using clean vs. tampered scenarios

Everything runs inside Docker and is triggered via:
```bash
make up && make demo
```

The system supports:
- End-to-end ingestion → hashing → logging → metrics
- Tamper-evident verification
- Evaluation of manipulated logs
- Metrics collection and output artifacts
- CI with automated testing and coverage

---

## Setup
Install dependencies and prepare environment:
```bash
make bootstrap
```

Build and start the container:
```bash
make up
```

Run the entire vertical slice:
```bash
make demo
```

---

## System Architecture
```text
+-----------------------+
|       src.app         |
|  (main pipeline)      |
| ingest → hash → log   |
+-----------+-----------+
            |
            v
+-----------------------+
|     logging.py        |
| append_log() writes   |
| seq, event, digest,   |
| prefix, bytes, sig    |
+-----------+-----------+
            |
            v
+-----------------------+
|    verify_logs.py     |
| recompute HMAC        |
| detect tampering      |
+-----------+-----------+
            |
            v
+-----------------------+
|     evaluate.py        |
| run clean + tampered   |
| scenarios, export CSV  |
+-----------------------+
```

All outputs are written to:
- `data/output/`
- `artifacts/release/`

---

## Runbook (Operations Guide)
1. Start the system
```bash
make up
```

2. Run full demonstration
```bash
make demo
```
This triggers:
- `python -m src.app`
- `python -m src.verify_logs`
- `python -m src.evaluate`

3. View output artifacts
```bash
ls data/output
ls artifacts/release
```

Key files:
| File                        | Description                               |
| --------------------------- | ----------------------------------------- |
| `logs.csv`                  | All tamper-evident log entries            |
| `hashes.json`               | Hash output from sample input             |
| `metrics.json`              | Summary of pipeline metrics               |
| `verification_results.json` | Verification pass/fail                    |
| `eval_metrics.csv`          | Evaluation of clean vs tampered scenarios |

4. Viewing verification results
```bash
cat artifacts/release/verification_results.json
```

5. Run tests
```bash
pytest --cov=src --cov-report=term-missing
```
CI automatically runs this on GitHub pushes.

6. Shut down system
```bash
docker-compose down
```
---

## Security Invariants
These rules ensure security-correctness and must never be violated.

### Invariant 1 — Plaintext logs alone are never trusted

Only logs that include:
- seq
- digest_prefix
- sig

are considered valid.

### Invariant 2 — Every log entry must include a cryptographic signature
Signatures are computed using:
- HMAC-SHA256
- Normalized (string-only) key–value pairs
- Deterministic JSON encoding

If the signature does not match → entry is tampered.

### Invariant 3 — Verification must be deterministic and reproducible
Given the same `logs.csv`, the verifier must always produce identical results.

### Invariant 4 — Tampering detection must be total

The system must detect modifications such as:
- Insertions
- Deletions
- Reordering
- In-place modification

Achieved through:
- HMAC mismatch
- Sequence analysis

### Invariant 5 — No sensitive data leaves the container
All logs and evaluation artifacts remain inside Docker:
- no outbound network traffic
- no production log ingestion
- synthetic data only

---

## What Works (Current State)
✔ ### End-to-end vertical slice
`make demo` runs:
1. app ingestion + hashing
2. tamper-evident logging
3. verification
4. evaluation scenarios

✔ ### Signatures now match correctly

`invalid_signatures:` 0 for untouched log files.

✔ ### Evaluation achieves desired behavior
- Clean → OK
- Tampered → FAIL

✔ ### CI is fully integrated
- Unit tests
- Negative tests
- Coverage
- Build & test workflow passes

✔ ### Docker reproducibility

Anyone can clone and run everything with:
```bash
make up && make demo
```

✔ ### Evidence collection
Artifacts stored in:
```arduino
artifacts/release/
```

---

## What’s Next (Future Improvements)

These are optional enhancements beyond project requirements:

### 1. Add per-entry asymmetric signatures

Use RSA or Ed25519 for stronger non-repudiation.

### 2. Add hash-chain checkpoints

Store periodic signed chain roots.

### 3. Log rotation with preserved chain integrity

Rotate logs.csv automatically but maintain continuity.

### 4. Expose metrics over a small Flask API

Live dashboard for log verification results.

### 5. Real-time stream verification

Continuously detect tampering attempts in near real time.

---

## Testing & CI
Test Categories
| Type          | File                 | Purpose                                |
| ------------- | -------------------- | -------------------------------------- |
| Happy Path    | `happy_path.py`      | Ensure correct behavior on valid input |
| Negative Test | `negative_test.py`   | Ensure failure on malformed input      |
| Unit Tests    | `unit_hashing.py`    | Isolated hashing correctness           |
| Edge Cases    | `test_edge_cases.py` | Unusual boundary behavior              |

Running Test Suite
```bash
pytest --cov=src --cov-report=term-missing
```
This produces a full source coverage table.

GitHub Actions (CI) automatically:
- Builds the Docker image
- Installs dependencies
- Runs all tests
- Publishes coverage summary
- Enforces quality gate

---

## Demo Video

---

## Evidence & Artifacts
After `make demo`, the following files are automatically generated:
```pgsql
artifacts/release/
  ├── verification_results.json
  ├── eval_metrics.csv
  └── (other logs/pcaps if added)
data/output/
  ├── logs.csv
  ├── hashes.json
  ├── metrics.json
  └── sample.txt processed output
```
These are required for the Beta milestone.

---

## Cleanup / Reset Instructions
If logs become corrupted during development:
```bash
rm -rf data/output
mkdir -p data/output
```

Re-run the system:
```bash
make up
make demo
```

For full cleanup:
```bash
docker system prune -af
```

---

## Repository Structure
```text
tamper-evident-logs/
│── src/
│   ├── app.py
│   ├── logging.py
│   ├── hashing.py
│   ├── metrics.py
│   ├── verify_logs.py
│   └── evaluate.py
│
│── tests/
│── data/input/
│── data/output/
│── artifacts/release/
│── docker-compose.yml
│── Dockerfile
│── Makefile
│── requirements.txt
│── README.md   
```
