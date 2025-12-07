import hashlib
from typing import Literal

Algo = Literal["sha256", "sha512", "md5"]

def hash_bytes(data: bytes, algo: Algo = "sha256") -> str:
    if algo == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algo == "sha512":
        return hashlib.sha512(data).hexdigest()
    elif algo == "md5":
        return hashlib.md5(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")

def hash_file(path: str, algo: Algo = "sha256", chunk_size: int = 65536) -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()
