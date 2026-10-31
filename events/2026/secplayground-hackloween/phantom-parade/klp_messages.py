"""Reassemble klp/2 DATA messages per stream and split into TLVs (tag u8, len u16be, value)."""
import pathlib, struct
from parse_klp import split_frames, parse

def message(path):
    frames = [parse(f) for f in split_frames(pathlib.Path(path).read_bytes())]
    data = [f for f in frames if f["typ"] == 2]
    total = {f["f2"] for f in data}
    assert len(total) == 1, total
    n = total.pop()
    frags = {}
    for f in data:                      # duplicates (retransmits) must carry identical payloads
        assert frags.setdefault(f["f1"], f["payload"]) == f["payload"]
    assert sorted(frags) == list(range(n)), sorted(frags)
    return b"".join(frags[i] for i in range(n)), frames

def tlvs(buf, off=5):
    out = []
    while off < len(buf):
        tag = buf[off]; ln = struct.unpack(">H", buf[off+1:off+3])[0]
        out.append((tag, buf[off+3:off+3+ln], ln)); off += 3 + ln
    return out, off

if __name__ == "__main__":
    for p in sorted(pathlib.Path("streams").glob("*_c2s.bin")):
        msg, _ = message(p)
        print("==", p.name, "msg len", len(msg), "hdr", msg[:5].hex())
        try:
            ts, end = tlvs(msg)
        except Exception as e:
            print("  TLV parse failed:", e); continue
        for tag, val, ln in ts:
            print(f"  tag 0x{tag:02x} len {ln:3} actual {len(val):3} {val[:60]!r}")
        print("  consumed", end, "of", len(msg))
