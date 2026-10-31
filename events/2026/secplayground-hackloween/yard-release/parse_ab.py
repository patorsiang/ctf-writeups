"""Parse an Android Backup (.ab) file: ANDROID BACKUP header (4 newline-terminated
lines: magic, version, compressed flag, encryption), followed by a zlib-compressed
tar stream when compressed=1 and encryption=none (the simple case this challenge
uses, confirmed by inspecting the header bytes with xxd).

Usage: python3 parse_ab.py <path.ab> <out_dir>
"""
import sys
import tarfile
import zlib
import io

def parse(path: str):
    data = open(path, "rb").read()
    lines = []
    pos = 0
    for _ in range(4):
        nl = data.index(b"\n", pos)
        lines.append(data[pos:nl].decode())
        pos = nl + 1
    magic, version, compressed, encryption = lines
    assert magic == "ANDROID BACKUP", magic
    payload = data[pos:]
    if compressed == "1":
        payload = zlib.decompress(payload)
    return dict(version=version, compressed=compressed, encryption=encryption), payload

if __name__ == "__main__":
    header, payload = parse(sys.argv[1])
    print("header:", header, "payload bytes:", len(payload))
    out_dir = sys.argv[2]
    try:
        tf = tarfile.open(fileobj=io.BytesIO(payload))
        tf.extractall(out_dir)
        for m in tf.getmembers():
            print(" ", m.name, m.size)
    except tarfile.TarError as e:
        print("not a tar, raw payload:", payload[:500])
