"""Exploratory: try cheap keys against klp/2 tag-0x21 blobs. Characterisation only (not a verified solve)."""
import pathlib, itertools, hashlib
from klp_messages import message, tlvs
from parse_klp import split_frames, parse

def load():
    streams = {}
    for p in sorted(pathlib.Path("streams").glob("s*_c2s.bin")):
        msg, frames = message(p)
        sid = parse(split_frames(p.read_bytes())[0])["sid"]
        d = {t: v for t, v, _ in tlvs(msg)[0]} if p.name[:3] != "s71" else {}
        streams[p.name] = dict(sid=sid, nonce=d.get(0x1f), blob=d.get(0x21), msg=msg)
    return streams

def xor_rep(data, key): return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
def printable(b): return sum(32 <= c < 127 for c in b) / max(len(b), 1)

if __name__ == "__main__":
    S = load()
    token = b"api_token=sk_live_7Ka2mQ9dR4tV1zXb8nH0pL"
    for name, s in S.items():
        if not s["blob"]: continue
        sid = s["sid"].to_bytes(2, "big")
        cands = {"nonce": s["nonce"], "sid": sid, "nonce+sid": s["nonce"] + sid, "sid+nonce": sid + s["nonce"],
                 "cid": b"4F2A9C", "host": b"WIN-4F2A9C", "token": token, "tokenval": b"sk_live_7Ka2mQ9dR4tV1zXb8nH0pL",
                 "sha256(nonce)": hashlib.sha256(s["nonce"]).digest(), "sha256(token)": hashlib.sha256(token).digest()}
        best = max(((printable(xor_rep(s["blob"], k)), n) for n, k in cands.items()))
        print(f"{name:32} nonce={s['nonce'].hex()} sid={sid.hex()} best={best[1]} {best[0]:.2f}")
        print("   blob", s["blob"].hex())
