"""Brute-force key x cipher x IV-layout over the klp/2 tag-0x21 blobs. Exploratory; hits must be verified by reconstruction."""
import hashlib, itertools, sys
from Crypto.Cipher import AES, ARC4, ChaCha20, Salsa20, DES3
from blob_try import load
from txt_blocks import txt_answers

S = {k: v for k, v in load().items() if v["blob"]}
TXT = txt_answers()
cfg = TXT["cfg.sync-telemetry-cdn.net"][1]
nodes = [TXT[f"node-{i:02d}.lanterns.hollowmere.test"][1] for i in range(12)]
token = b"sk_live_7Ka2mQ9dR4tV1zXb8nH0pL"
base = {"cfg": cfg, "nodes_cat": b"".join(nodes), "token": token, "api_token=": b"api_token=" + token,
        "host": b"WIN-4F2A9C", "cid": b"4F2A9C", "uid": b"SYSTEM", "klp": b"klp/2", "banner": b"klp/2 implant online; host=WIN-4F2A9C; uid=SYSTEM",
        "hello": b"v=2;os=win;arch=x64;cid=4F2A9C", "beacon": b"beacon interval=45s jitter=20%", "dom": b"sync-telemetry-cdn.net",
        "hollow": b"hollowmere", "lanterns": b"lanterns", "exfil": b"exfiltrate.net", "dnscred": b"svc-backup:Restore#Wgx7Q2r!vpn-2024"}
for i, n in enumerate(nodes): base[f"node{i:02d}"] = n


base["icmpkey"] = bytes.fromhex("e33116fe6443a1ae100e28f31420feb3")
base["aws_id"] = b"AKIA4NP7QF2ZK9RTBX3L"
base["aws_secret"] = b"hV3+8Qk2n0pWm1sZbAeR7yT4uXcL6oDgJfHi5rEq"
base["dbpass"] = b"S3ason!2024"; base["dburl"] = b"postgres://ops:S3ason!2024@db-prod-01.internal:5432/billing"
base["cred_user"] = b"svc-backup"; base["cred_pass"] = b"Restore#Wgx7Q2r!vpn-2024"; base["cred_tail"] = b"Wgx7Q2r!vpn-2024"
base["dbhost"] = b"db-prod-01.internal"

def keys_for(s):
    nonce, sid = s["nonce"], s["sid"].to_bytes(2, "big")
    for name, k in base.items():
        for tag, kk in [("", k), ("+n", k + nonce), ("n+", nonce + k), ("+sid", k + sid), ("+n+sid", k + nonce + sid)]:
            yield name + tag, kk
            for hn, h in [("md5", hashlib.md5), ("sha1", hashlib.sha1), ("sha256", hashlib.sha256)]:
                d = h(kk).digest(); yield f"{hn}({name}{tag})", d; yield f"{hn}({name}{tag})[:16]", d[:16]
    for pair in itertools.permutations(["cfg", "host", "token", "cid"], 2):
        yield "+".join(pair), base[pair[0]] + base[pair[1]]
    yield "cfg^nonce*", bytes(c ^ nonce[i % 4] for i, c in enumerate(cfg))

def ivs(s):
    n, sid = s["nonce"], s["sid"].to_bytes(2, "big")
    yield "zero", bytes(16); yield "n|0", n + bytes(12); yield "0|n", bytes(12) + n
    yield "n*4", n * 4; yield "sid|0", sid + bytes(14); yield "n+sid|0", n + sid + bytes(10)

def printable(b): return sum(32 <= c < 127 for c in b) / max(len(b), 1)

def attempts(s, key):
    ct = s["blob"]
    if key: yield "xor", bytes(b ^ key[i % len(key)] for i, b in enumerate(ct))
    yield "rc4", ARC4.new(key).decrypt(ct) if 1 <= len(key) <= 256 else b""
    if len(key) in (16, 24, 32):
        for iv_n, iv in ivs(s):
            yield f"ctr-iv:{iv_n}", AES.new(key, AES.MODE_CTR, initial_value=iv, nonce=b"").decrypt(ct)
            yield f"cfb-{iv_n}", AES.new(key, AES.MODE_CFB, iv=iv, segment_size=8).decrypt(ct)
            yield f"ofb-{iv_n}", AES.new(key, AES.MODE_OFB, iv=iv).decrypt(ct)
            if len(ct) % 16 == 0: yield f"cbc-{iv_n}", AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ct)
        # iv-prefixed layouts
        yield "ctr-prefix8", AES.new(key, AES.MODE_CTR, nonce=ct[:8]).decrypt(ct[8:])
        yield "ctr-prefix12", AES.new(key, AES.MODE_CTR, nonce=ct[:12]).decrypt(ct[12:])
        yield "cbc-prefix16", AES.new(key, AES.MODE_CBC, iv=ct[:16]).decrypt(ct[16:][: (len(ct) - 16) // 16 * 16]) if len(ct) > 16 else b""
        if len(ct) % 16 == 0: yield "ecb", AES.new(key, AES.MODE_ECB).decrypt(ct)
    if len(key) == 32:
        for nn_n, nn in [("n|0(8)", s["nonce"] + bytes(4)), ("0(8)", bytes(8))]:
            yield f"chacha-{nn_n}", ChaCha20.new(key=key, nonce=nn).decrypt(ct)
            yield f"salsa-{nn_n}", Salsa20.new(key=key, nonce=nn).decrypt(ct)
        yield "chacha-prefix8", ChaCha20.new(key=key, nonce=ct[:8]).decrypt(ct[8:])

hits = []
for name, s in S.items():
    for kn, key in keys_for(s):
        for an, pt in attempts(s, key):
            if not pt: continue
            sc = printable(pt)
            if sc > 0.80 or b"forensic" in pt or b"flag" in pt.lower():
                hits.append((sc, name[:3], kn, an, pt[:70]))
hits.sort(reverse=True)
print("hits:", len(hits))
for h in hits[:25]: print(h)
