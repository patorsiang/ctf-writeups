from decrypt_payload import decrypt, RAND, BLOB

def test_hmac_prefix_matches_so_key_is_right():
    r = decrypt(BLOB.read_bytes(), RAND)
    assert r["mac_ok_truncated"]

def test_plaintext_is_text():
    r = decrypt(BLOB.read_bytes(), RAND)
    r["plain"].decode("utf8")
