from pathlib import Path
from .hashing import hash_bytes, hash_file
from .logging_utils import append_log
from .metrics import export_metrics
from .security import validate_input_text, validate_algo

def run_text_pipeline(text: str, algo: str = "sha256") -> dict:
    validate_input_text(text)
    validate_algo(algo)

    append_log("ingest", {"source": "text", "algo": algo, "size": len(text)})
    digest = hash_bytes(text.encode(), algo=algo)
    append_log("encrypt", {"algo": algo, "digest_prefix": digest[:12]})
    result = {"algo": algo, "digest": digest, "len": len(text)}

    metrics = {"items_hashed": 1, "algo": algo, "avg_len": len(text)}
    export_metrics(metrics)
    append_log("summarize", {"items": 1})

    return result

def run_file_pipeline(path: str, algo: str = "sha256") -> dict:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    validate_algo(algo)

    append_log("ingest", {"source": "file", "algo": algo, "path": str(p)})
    digest = hash_file(str(p), algo=algo)
    append_log("encrypt", {"algo": algo, "digest_prefix": digest[:12]})
    result = {"algo": algo, "digest": digest, "bytes": p.stat().st_size}

    metrics = {"items_hashed": 1, "algo": algo, "total_bytes": p.stat().st_size}
    export_metrics(metrics)
    append_log("summarize", {"items": 1})

    return result
