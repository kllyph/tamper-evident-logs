from src.pipeline import run_text_pipeline

def test_happy_text_sha256():
    out = run_text_pipeline("abc", algo="sha256")
    assert out["algo"] == "sha256"
    assert len(out["digest"]) == 64  # sha256 hex length
