from src.hashing import hash_bytes

def test_hash_bytes_md5():
    digest = hash_bytes(b"abc", "md5")
    assert digest == "900150983cd24fb0d6963f7d28e17f72"
