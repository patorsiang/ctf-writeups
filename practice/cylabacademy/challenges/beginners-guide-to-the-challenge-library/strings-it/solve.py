"""strings it — find a literal in a binary without running it.

`strings file | grep -i pico` solves this in one line. This file
reimplements the scan, because what `strings` actually does is the
lesson and it is only three rules:

  1. walk the bytes looking for runs of *printable* characters
  2. a run ends at the first non-printable byte (usually the NUL that
     terminates a C string)
  3. emit runs of at least `min_len` characters, discard shorter ones

Nothing is executed and nothing is parsed as a binary format, which is
why the target's OS and CPU are irrelevant -- the same reason this
challenge needs no Docker while Wave a Flag did.

    python3 solve.py                  # scan the challenge file
    python3 solve.py FILE             # scan another file
    python3 solve.py FILE --all       # print every string, not just flags
"""

import re
import sys
from pathlib import Path

# GNU strings treats the printable ASCII range as printable, plus tab.
PRINTABLE = set(range(0x20, 0x7F)) | {0x09}

FLAG_RE = re.compile(r"[a-zA-Z0-9_]*CTF\{[^}]*\}", re.IGNORECASE)

TARGET = Path(__file__).parent / "strings"


def extract_strings(data: bytes, min_len: int = 4, encoding: str = "ascii"):
    """Yield (offset, text) for every printable run of at least min_len.

    encoding="ascii" is one byte per character, the default everywhere.
    encoding="utf-16le" reads printable bytes separated by NULs, which is
    how Windows binaries store text -- an ASCII-only scan finds *nothing*
    in them, and that silent miss is worth knowing about.
    """
    if encoding == "ascii":
        step, offset_of = 1, lambda start: start
    elif encoding == "utf-16le":
        step, offset_of = 2, lambda start: start
    else:
        raise ValueError(f"unsupported encoding {encoding!r}")

    run: list[str] = []
    start = 0
    i = 0
    while i < len(data):
        byte = data[i]
        wide_ok = encoding == "ascii" or (i + 1 < len(data) and data[i + 1] == 0)

        if byte in PRINTABLE and wide_ok:
            if not run:
                start = i
            run.append(chr(byte))
            i += step
            continue

        if len(run) >= min_len:
            yield offset_of(start), "".join(run)
        run = []
        i += 1 if encoding == "ascii" else 1

    if len(run) >= min_len:
        yield offset_of(start), "".join(run)


def find_flags(data: bytes, min_len: int = 4) -> list[tuple[int, str]]:
    """Flag-shaped strings, ASCII and UTF-16LE, deduplicated by text."""
    seen: dict[str, int] = {}
    for encoding in ("ascii", "utf-16le"):
        for offset, text in extract_strings(data, min_len, encoding):
            for match in FLAG_RE.findall(text):
                seen.setdefault(match, offset)
    return sorted((offset, text) for text, offset in seen.items())


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(args[0]) if args else TARGET

    if not path.exists():
        sys.exit(f"{path} not found — download it from the challenge page")

    data = path.read_bytes()

    if "--all" in sys.argv:
        for offset, text in extract_strings(data):
            print(f"{offset:8x}  {text}")
    else:
        found = find_flags(data)
        if not found:
            sys.exit("no flag-shaped strings found; try --all")
        for offset, text in found:
            print(f"FLAG @ 0x{offset:x}: {text}")
