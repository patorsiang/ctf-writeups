"""Targeted: blob lengths (80/88) are ciphertext+16-byte GCM tag len off-by-16 of block size.
Try AES-GCM with tag = blob[-16:], ct = blob[:-16], over the same candidate key/nonce space."""
import hashlib, itertools
from Crypto.Cipher import AES
from blob_try import load
from txt_blocks import txt_answers

S = {k: v for k, v in load().items() if v["blob"]}
TXT = txt_answers()
cfg = TXT["cfg.sync-telemetry-cdn.net"][1]
nodes = [TXT[f"node-{i:02d}.lanterns.hollowmere.test"][1] for i in range(12)]
token = b"sk_live_7Ka2mQ9dR4tV1zXb8nH0pL"
base = {"cfg": cfg, "nodes_cat": b"".join(nodes), "token": token, "api_token=": b"api_token=" + token,
        "host": b"WIN-4F2A9C", "cid": b"4F2A9C", "uid": b"SYSTEM", "klp": b"klp/2",
        "banner": b"klp/2 implant online; host=WIN-4F2A9C; uid=SYSTEM",
        "hello": b"v=2;os=win;arch=x64;cid=4F2A9C", "beacon": b"beacon interval=45s jitter=20%",
        "dom": b"sync-telemetry-cdn.net", "hollow": b"hollowmere", "lanterns": b"lanterns",
        "exfil": b"exfiltrate.net", "dnscred": b"svc-backup:Restore#Wgx7Q2r!vpn-2024",
        "icmpkey": bytes.fromhex("e33116fe6443a1ae100e28f31420feb3"),
        "aws_id": b"AKIA4NP7QF2ZK9RTBX3L",
        "aws_secret": b"hV3+8Qk2n0pWm1sZbAeR7yT4uXcL6oDgJfHi5rEq",
        "dbpass": b"S3ason!2024", "cred_tail": b"Wgx7Q2r!vpn-2024", "cred_pass": b"Restore#Wgx7Q2r!vpn-2024"}
for i, n in enumerate(nodes): base[f"node{i:02d}"] = n

def keys_for(s):
    nonce, sid = s["nonce"], s["sid"].to_bytes(2, "big")
    for name, k in base.items():
        for tag, kk in [("", k), ("+n", k + nonce), ("n+", nonce + k), ("+sid", k + sid)]:
            for hn, h in [("md5", hashlib.md5), ("sha1", hashlib.sha1), ("sha256", hashlib.sha256)]:
                d = h(kk).digest()
                yield f"{hn}({name}{tag})", d[:16]
                yield f"{hn}({name}{tag})32", d[:32] if len(d) >= 32 else None

def nonces_for(s):
    n, sid = s["nonce"], s["sid"].to_bytes(2, "big")
    yield "raw4", n
    yield "n+0x8", n + bytes(8)
    yield "n+sid+0x6", n + sid + bytes(6)
    yield "0x8+n", bytes(8) + n
    yield "n*3", n * 3
    yield "sid+n+0x6", sid + n + bytes(6)

hits = []
for name, s in S.items():
    blob = s["blob"]
    if len(blob) <= 16:
        continue
    ct, tagb = blob[:-16], blob[-16:]
    for kn, key in keys_for(s):
        if not key:
            continue
        for nn, nonce in nonces_for(s):
            try:
                c = AES.new(key, AES.MODE_GCM, nonce=nonce)
                pt = c.decrypt_and_verify(ct, tagb)
                hits.append((name, kn, nn, pt))
            except Exception:
                pass
print("hits:", len(hits))
for h in hits[:20]:
    print(h)
