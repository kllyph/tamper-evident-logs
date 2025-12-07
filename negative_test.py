import pytest
from src.pipeline import run_text_pipeline

def test_negative_empty_input():
    with pytest.raises(ValueError):
        run_text_pipeline("", algo="sha256")
