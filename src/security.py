import re

def validate_input_text(s: str, max_len: int = 1_000_000) -> None:
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    if len(s) == 0:
        raise ValueError("Input cannot be empty")
    if len(s) > max_len:
        raise ValueError("Input too large")
    # Basic rate limiting / simplistic sanity checks would be elsewhere,
    # but this demonstrates input validation.

def validate_algo(algo: str) -> None:
    if algo not in {"sha256", "sha512", "md5"}:
        raise ValueError("Unsupported algorithm")
