"""Characterisation tests for the Too Loud To Yap recon phase.

These pin the *observations* that narrowed the cipher family, so the writeup
can be reconstructed and so a wrong turn later gets caught immediately.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import re
from collections import Counter
from pathlib import Path

CT_PATH = Path(__file__).parent / "ct.txt"
WORDLIST = Path("/usr/share/dict/words")

ENGLISH_IC = 0.066
RANDOM_IC = 0.038


def load_stream():
    """Letters-only ciphertext stream, with the ALL-CAPS crib words removed.

    The cribs are plaintext the author leaked; leaving them in would pollute
    any statistic we run over the ciphertext.
    """
    text = CT_PATH.read_text()
    without_cribs = re.sub(r"\b[A-Z]{3,}\b", "", text)
    return re.sub(r"[^A-Za-z]", "", without_cribs).lower()


def index_of_coincidence(s):
    n = len(s)
    if n < 2:
        return 0.0
    counts = Counter(s)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def average_column_ic(s, k):
    """Split into k columns and average their IC — the standard Vigenere probe.

    If the key repeats with period k, each column is a single Caesar shift and
    its IC jumps to roughly English (0.066).
    """
    columns = [s[i::k] for i in range(k)]
    return sum(index_of_coincidence(c) for c in columns) / k


def subtract(ct, pt):
    """key = ct - pt (mod 26), the Vigenere/running-key recovery step."""
    return "".join(
        chr((ord(c) - ord(p)) % 26 + ord("a")) for c, p in zip(ct.lower(), pt.lower())
    )


def caesar(word, shift):
    return "".join(chr((ord(c) - ord("a") + shift) % 26 + ord("a")) for c in word)


def test_no_repeating_key_up_to_length_15():
    """Rules out classic Vigenere: no key length shows an English-like IC."""
    stream = load_stream()
    scores = {k: average_column_ic(stream, k) for k in range(1, 16)}

    worst = max(scores.values())
    assert worst < 0.050, f"a key length looks periodic now: {scores}"

    # And it is not merely 'below English' — it sits down at random-text level.
    midpoint = (ENGLISH_IC + RANDOM_IC) / 2
    assert all(v < midpoint for v in scores.values()), scores


def test_word_level_caesar_is_ruled_out():
    """Rules out per-word Caesar: no garbage word rotates into a real word."""
    if not WORDLIST.exists():
        return  # dictionary is platform-dependent; skip rather than fail
    words = {w.strip().lower() for w in WORDLIST.read_text().splitlines()}

    # Words already readable in the ciphertext are not evidence either way.
    known_plaintext = {"here", "thing", "that", "then", "next"}
    tokens = [
        t.replace("'", "").lower()
        for t in re.findall(r"[A-Za-z']+", CT_PATH.read_text())
        if not (t.isupper() and len(t) > 2)
    ]
    garbage = [t for t in tokens if len(t) >= 4 and t not in known_plaintext]
    assert len(garbage) > 40, "sanity: expected plenty of encrypted words"

    hits = [t for t in garbage if any(caesar(t, k) in words for k in range(1, 26))]
    # A couple of short words rotate into obscure dictionary entries by chance;
    # what matters is that it is noise, not a consistent shift.
    assert len(hits) / len(garbage) < 0.10, f"unexpectedly many Caesar hits: {hits}"


def test_caps_words_are_cribs_yielding_english_key():
    """The load-bearing finding: ALL-CAPS words decode the ciphertext before
    them, and ct - crib produces English prose, i.e. a running key."""
    # (ciphertext as written, plaintext given by the adjacent crib, key fragment)
    cases = [
        ("oo", "at", "ov"),  # oo  xyc ATTHE hospiaod
        ("xyc", "the", "ery"),  #      -> "at the hospital"
        ("iwope", "movie", "witha"),  # o iwope MOVIEA -> "a movie"
        ("xyetw", "quite", "hewas"),  # xyetw QUITE    -> "quite"
    ]
    for ct, pt, expected_key in cases:
        assert subtract(ct, pt) == expected_key, f"{ct} - {pt}"

    # Adjacent cribs concatenate into running prose rather than repeating.
    assert subtract("ooxyc", "atthe") == "overy"


def test_ciphertext_is_unmodified():
    """Guards the artifact itself — solve scripts are worthless if the input
    silently changes."""
    raw = CT_PATH.read_bytes()
    assert len(raw) == 781, "ct.txt changed size; recon results are stale"
    assert b"lactf{" in raw, "flag ciphertext missing from ct.txt"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
