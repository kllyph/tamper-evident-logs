import pytest
from src.pipeline import run_text_pipeline

def test_edge_large_input():
    s = "a" * 10000
    out = run_text_pipeline(s, algo="sha512")
    assert out["algo"] == "sha512"
    assert len(out["digest"]) == 128  # sha512 hex length

def test_negative_unsupported_algo():
    with pytest.raises(ValueError):
        run_text_pipeline("abc", algo="sha3-256")
