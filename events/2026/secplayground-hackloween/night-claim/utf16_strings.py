"""Extract printable UTF-16LE runs (len>=min_len) from a binary file, e.g. Android binary XML.

Usage: python3 utf16_strings.py <path> [min_len]
"""
import sys

def utf16le_strings(data: bytes, min_len: int = 4):
    out, cur = [], []
    i = 0
    while i + 1 < len(data):
        lo, hi = data[i], data[i + 1]
        if hi == 0 and 0x20 <= lo < 0x7F:
            cur.append(chr(lo))
        else:
            if len(cur) >= min_len:
                out.append("".join(cur))
            cur = []
        i += 2
    if len(cur) >= min_len:
        out.append("".join(cur))
    return out

if __name__ == "__main__":
    path = sys.argv[1]
    min_len = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    data = open(path, "rb").read()
    for s in utf16le_strings(data, min_len):
        print(s)
