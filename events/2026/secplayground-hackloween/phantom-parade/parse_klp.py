"""Parse klp/2 frames from reassembled c2s stream dumps (see dump_streams.py).

Layout inferred by eye, then CHECKED by tests (test_klp.py), not assumed:
  magic(3)=c3 7a 02 | type(1) | sid(2) | seq(2) | f1(2) | f2(2) | len(2) | chk(2) | payload(len)
"""
import pathlib, struct, sys

MAGIC = b"\xc3\x7a\x02"

def split_frames(buf: bytes):
    idx = [i for i in range(len(buf)) if buf.startswith(MAGIC, i)]
    idx.append(len(buf))
    return [buf[a:b] for a, b in zip(idx, idx[1:])]

def parse(frame: bytes):
    typ = frame[3]
    sid, seq, f1, f2, ln, chk = struct.unpack(">HHHHHH", frame[4:16])
    return dict(typ=typ, sid=sid, seq=seq, f1=f1, f2=f2, ln=ln, chk=chk,
                payload=frame[16:16 + ln], rest=frame[16 + ln:])

if __name__ == "__main__":
    for p in sorted(pathlib.Path("streams").glob("*_c2s.bin")):
        print("==", p.name)
        for fr in split_frames(p.read_bytes()):
            d = parse(fr)
            print(f"  t{d['typ']} sid={d['sid']:04x} seq={d['seq']} f1={d['f1']} f2={d['f2']} ln={d['ln']} "
                  f"chk={d['chk']:04x} pl={d['payload'][:24].hex()}.. rest={d['rest'].hex()}")
