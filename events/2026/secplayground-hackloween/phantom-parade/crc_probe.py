"""Probe: are the 4-byte fields (tag 0x1f, type-3 trailers) a CRC/hash of something we can see?"""
import zlib, hashlib, pathlib, itertools
from blob_try import load
from klp_messages import message
from parse_klp import split_frames, parse

S = load()
for name, s in S.items():
    if not s["blob"]: continue
    p = pathlib.Path("streams") / name
    frames = [parse(f) for f in split_frames(p.read_bytes())]
    t3 = [f["payload"] for f in frames if f["typ"] == 3]
    hello = [f["payload"] for f in frames if f["typ"] == 1][0]
    msg = s["msg"]; blob = s["blob"]; n = s["nonce"]
    targets = {"nonce(1f)": n, "t3[0]": t3[0], "t3[1]": t3[1]}
    pools = {"hello": hello, "msg": msg, "msg[5:]": msg[5:], "blob": blob, "blob[:-4]": blob[:-4], "blob[4:]": blob[4:],
             "banner": b"klp/2 implant online; host=WIN-4F2A9C; uid=SYSTEM", "token": msg[5+3+49+3:5+3+49+3+40],
             "sid": s["sid"].to_bytes(2, "big")}
    hits = []
    for (tn, tv), (pn, pv) in itertools.product(targets.items(), pools.items()):
        for fn, f in [("crc32", lambda b: zlib.crc32(b).to_bytes(4, "big")), ("adler", lambda b: zlib.adler32(b).to_bytes(4, "big")),
                      ("crc32le", lambda b: zlib.crc32(b).to_bytes(4, "little")),
                      ("sha256[:4]", lambda b: hashlib.sha256(b).digest()[:4]), ("md5[:4]", lambda b: hashlib.md5(b).digest()[:4]),
                      ("sha1[:4]", lambda b: hashlib.sha1(b).digest()[:4])]:
            if f(pv) == tv: hits.append((tn, fn, pn))
    print(name, "hits:", hits)
