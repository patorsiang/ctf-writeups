"""Offline decrypt of the font-disguised C2 payload. Layout from install-hook.js:
magic 'ttcf' | mac[16] | iv[16] | aes-256-cbc ct. key = sha256(rand8 || seed)."""
import hashlib
import hmac
import subprocess
from pathlib import Path

BLOB = Path(__file__).parent / "artifacts/payload.bin"
RAND = bytes.fromhex("342c039da25a7069")  # from X-Font-Range request header
SEED = b"a13b5995066140a0"


def decrypt(blob: bytes, rand: bytes) -> dict:
    assert blob[:4] == b"ttcf"
    mac, iv, ct = blob[4:0x14], blob[0x14:0x24], blob[0x24:]
    key = hashlib.sha256(rand + SEED).digest()
    full = hmac.new(key, iv + ct, hashlib.sha256).digest()
    plain = subprocess.run(
        ["openssl", "enc", "-d", "-aes-256-cbc", "-K", key.hex(), "-iv", iv.hex()],
        input=ct, capture_output=True, check=True,
    ).stdout
    return {"mac_ok_truncated": full[:16] == mac, "mac_ok_full": full == mac, "plain": plain}


if __name__ == "__main__":
    r = decrypt(BLOB.read_bytes(), RAND)
    print({k: v for k, v in r.items() if k != "plain"})
    Path(__file__).parent.joinpath("artifacts/gh.ps1.txt").write_bytes(r["plain"])
    print(r["plain"].decode("utf8", "replace")[:4000])
