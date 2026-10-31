"""Probe the 16-bit chk field: find a formula over payload/header fields that holds for ALL frames."""
import pathlib, zlib
from parse_klp import split_frames, parse

frames = []
for p in sorted(pathlib.Path("streams").glob("s*_c2s.bin")):
    for f in split_frames(p.read_bytes()):
        d = parse(f); d["stream"] = p.name[:3]; d["raw"] = f; frames.append(d)

def sum16(b): return sum(b) & 0xFFFF
tests = {
    "sum(payload)":            lambda d: sum16(d["payload"]),
    "sum(payload)+seq":        lambda d: (sum16(d["payload"]) + d["seq"]) & 0xFFFF,
    "sum(payload)+typ":        lambda d: (sum16(d["payload"]) + d["typ"]) & 0xFFFF,
    "sum(payload)+seq+typ":    lambda d: (sum16(d["payload"]) + d["seq"] + d["typ"]) & 0xFFFF,
    "sum(raw[3:16])+sum(pl)":  lambda d: (sum16(d["raw"][3:14]) + sum16(d["payload"])) & 0xFFFF,
    "sum(raw[3:14])":          lambda d: sum16(d["raw"][3:14]),
    "crc16-ish(crc32&ffff)":   lambda d: zlib.crc32(d["payload"]) & 0xFFFF,
}
for n, fn in tests.items():
    ok = sum(fn(d) == d["chk"] for d in frames)
    print(f"{n:26} {ok}/{len(frames)}")
# show residual chk - sum(payload) for a few frames
print("residuals (chk - sum(payload)) mod 65536:")
for d in frames[:14]:
    print(f"  {d['stream']} t{d['typ']} seq={d['seq']} f1={d['f1']} f2={d['f2']} ln={d['ln']} resid={(d['chk']-sum16(d['payload']))&0xFFFF}")
