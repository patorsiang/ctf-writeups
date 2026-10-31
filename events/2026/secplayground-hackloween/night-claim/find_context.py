"""Find a needle in a binary file and print a wide printable-ASCII window around it.

`strings` truncates at non-printable bytes, which can hide the start/end of a
length-prefixed string (as in Dalvik's MUTF-8 string pool). This looks at the
raw bytes directly instead of trusting strings' boundaries.
"""
import sys

def printable_window(data: bytes, idx: int, before: int = 40, after: int = 120):
    lo = max(0, idx - before)
    hi = min(len(data), idx + after)
    chunk = data[lo:hi]
    return "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)

if __name__ == "__main__":
    path, needle = sys.argv[1], sys.argv[2].encode()
    data = open(path, "rb").read()
    start = 0
    while True:
        idx = data.find(needle, start)
        if idx == -1:
            break
        print(f"@{idx}: {printable_window(data, idx)}")
        start = idx + 1
