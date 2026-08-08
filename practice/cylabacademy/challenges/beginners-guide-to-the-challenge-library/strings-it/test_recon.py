"""Tests for strings it.

The system `strings` is the oracle: a from-scratch reimplementation is
only worth having if it agrees with the real tool on a real 768 KB
binary, not just on toy inputs.

The challenge file is large and may not be present in a fresh clone, so
tests needing it skip rather than fail. Tests that need no fixture --
the scan rules themselves -- always run.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import shutil
import subprocess

from solve import TARGET, extract_strings, find_flags

FLAG = "picoCTF{5tRIng5_1T_1067EC4c}"
FLAG_OFFSET = 0x1CAA0


class Skip(Exception):
    """Raised when a fixture the test needs is unavailable."""


def _target_bytes():
    if not TARGET.exists():
        raise Skip(f"{TARGET.name} not present")
    return TARGET.read_bytes()


# --------------------------------------------------------------------------
# Against the real challenge binary
# --------------------------------------------------------------------------


def test_finds_the_flag_in_the_challenge_binary():
    found = find_flags(_target_bytes())
    assert found == [(FLAG_OFFSET, FLAG)], found


def test_flag_is_a_plain_nul_terminated_literal():
    """Why `strings` finds it at all: the flag is a C string literal in
    .rodata, stored verbatim and NUL-terminated -- not encoded, not
    computed at runtime."""
    data = _target_bytes()
    assert data[FLAG_OFFSET : FLAG_OFFSET + len(FLAG)] == FLAG.encode()
    assert data[FLAG_OFFSET - 1] == 0
    assert data[FLAG_OFFSET + len(FLAG)] == 0


def test_matches_the_system_strings_exactly():
    """The differential test that makes the reimplementation credible:
    identical output to GNU/BSD strings over 768 KB of real binary."""
    if shutil.which("strings") is None:
        raise Skip("system `strings` not on PATH")
    data = _target_bytes()

    mine = {text for _, text in extract_strings(data, min_len=4)}
    theirs = set(
        subprocess.run(
            ["strings", "-n", "4", str(TARGET)],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    )
    assert mine == theirs, f"+{len(mine - theirs)} / -{len(theirs - mine)}"


# --------------------------------------------------------------------------
# The three scan rules, on inputs small enough to reason about
# --------------------------------------------------------------------------


def test_run_shorter_than_min_len_is_discarded():
    assert list(extract_strings(b"\x00abc\x00", min_len=4)) == []
    assert list(extract_strings(b"\x00abcd\x00", min_len=4)) == [(1, "abcd")]


def test_min_len_is_configurable():
    assert list(extract_strings(b"\x00abc\x00", min_len=3)) == [(1, "abc")]


def test_non_printable_byte_ends_a_run():
    assert list(extract_strings(b"hello\x01world", min_len=4)) == [
        (0, "hello"),
        (6, "world"),
    ]


def test_offsets_point_at_the_first_character():
    data = b"\xff" * 10 + b"marker" + b"\x00"
    assert list(extract_strings(data, min_len=4)) == [(10, "marker")]


def test_trailing_run_at_end_of_data_is_emitted():
    """A run that reaches the end of the file without a terminator must
    still be reported -- an off-by-one here silently drops the last
    string in every file."""
    assert list(extract_strings(b"\x00tail", min_len=4)) == [(1, "tail")]


def test_tab_counts_as_printable_but_newline_does_not():
    assert list(extract_strings(b"a\tbc", min_len=4)) == [(0, "a\tbc")]
    assert list(extract_strings(b"ab\ncd", min_len=4)) == []


# --------------------------------------------------------------------------
# UTF-16: the silent miss worth knowing about
# --------------------------------------------------------------------------


def test_ascii_scan_misses_utf16_text():
    """Windows binaries store text as UTF-16LE. An ASCII-only scan finds
    nothing -- it does not error, it just returns empty, which is why a
    "no strings found" result is not evidence of no strings."""
    wide = "SECRET_VALUE".encode("utf-16le")
    assert list(extract_strings(wide, min_len=4, encoding="ascii")) == []


def test_utf16_scan_finds_it():
    wide = b"\x00\x00" + "SECRET_VALUE".encode("utf-16le") + b"\x00\x00"
    found = [text for _, text in extract_strings(wide, min_len=4, encoding="utf-16le")]
    assert "SECRET_VALUE" in found, found


def test_find_flags_covers_both_encodings():
    wide = b"junk" + "picoCTF{wide_flag}".encode("utf-16le") + b"\x00\x00"
    assert [t for _, t in find_flags(wide)] == ["picoCTF{wide_flag}"]


def test_unsupported_encoding_raises():
    try:
        list(extract_strings(b"abcd", encoding="ebcdic"))
        assert False, "expected ValueError for an unsupported encoding"
    except ValueError:
        pass


if __name__ == "__main__":
    passed = skipped = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
                passed += 1
            except Skip as why:
                print(f"SKIP {name} ({why})")
                skipped += 1
    print(f"\n{passed} passed, {skipped} skipped")
