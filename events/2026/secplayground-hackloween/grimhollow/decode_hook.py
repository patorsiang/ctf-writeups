"""Statically decode the string table of hushkit-crypto install-hook.js. Never executes the sample."""
import base64
import re
import sys
from pathlib import Path

HOOK = Path(__file__).parent / "artifacts/install-hook.js.txt"
KEY_BYTES = [0x66, 0x4B, 0x03, 0x1F, 0x78, 0x43, 0x02, 0x78]
KEY = "".join(chr((x ^ 0x2D) + 3) for x in KEY_BYTES)


def load_table(src: str) -> list[str]:
    body = re.search(r"const _0x2a7c=\[(.*?)\];", src, re.S).group(1)
    return re.findall(r"'([^']*)'", body)


def decode_from(table: list[str], j: int) -> str:
    i = (j * 5 + 2) % len(table)
    raw = table[i][::-1]
    raw += "=" * (-len(raw) % 4)
    b = base64.b64decode(raw)
    return bytes(c ^ ord(KEY[(x + i) % len(KEY)]) for x, c in enumerate(b)).decode("utf8", "replace")


def decode(j: int) -> str:
    return decode_from(load_table(HOOK.read_text()), j)


if __name__ == "__main__":
    t = load_table(HOOK.read_text())
    for j in range(0x20):
        print(hex(j), repr(decode_from(t, j)))
