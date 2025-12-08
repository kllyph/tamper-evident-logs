### Khoa Vu – Technical Implementation Lead
- Implemented the core end-to-end pipeline (`src/app.py`), including controlled data ingestion, SHA-256 hashing, and digest summarization.
- Designed and implemented the tamper-evident logging subsystem (logging.py), including deterministic field normalization, signature generation using HMAC-SHA256, and per-entry metadata collection.
- Built the full Dockerized environment (Dockerfile, docker-compose.yml) and automated build/run process with make up and make demo.
- Implemented the log verification module (verify_logs.py), sequence gap analysis, and tampering detection logic.
- Created evaluation scenarios (evaluate.py) that compare clean vs. tampered logs and export CSV metrics.
- Integrated CI pipeline with unit tests, negative tests, and coverage reporting.

### Kelly Pham – Documentation, Metrics, and Testing Lead
- Designed overall project architecture diagram, workflow, and structured documentation including README, runbook, and security invariants.
- Implemented metrics collection logic (metrics.py) to produce reproducible summaries (metrics.json) and integrated artifact generation in artifacts/release/.
- Contributed to structured CSV log formatting and ensured compatibility between logging and verification modules.
- Wrote and refined happy-path tests, edge-case tests, and negative input tests to ensure correctness and robustness.
- Assisted in debugging HMAC mismatches, signature normalization issues, and Docker mount inconsistencies.
- Prepared the final presentation slides, demo script, and evaluation summary.
