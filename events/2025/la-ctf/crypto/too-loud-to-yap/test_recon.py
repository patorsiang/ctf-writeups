"""Tests for Too Loud To Yap.

Two kinds live here, deliberately:

  * Correctness — the autokey model reproduces ct.txt exactly and yields the
    flag from the ciphertext alone.
  * Characterisation — the eliminations from the recon phase, kept because
    they are the reusable part and because they explain why the wrong path
    looked plausible for as long as it did.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import re
from collections import Counter
from pathlib import Path

from solve import PRIMER, decrypt, encrypt, find_flag, letters

CT_PATH = Path(__file__).parent / "ct.txt"
FLAG = "lactf{down_with_cis_bus}"

ENGLISH_IC = 0.066
RANDOM_IC = 0.038


# --------------------------------------------------------------------------
# Correctness
# --------------------------------------------------------------------------


def test_solve_recovers_the_flag():
    assert find_flag(decrypt(letters(CT_PATH.read_text()))) == FLAG


def test_model_reproduces_the_ciphertext_exactly():
    """The real proof. Decrypting to something readable is suggestive;
    re-encrypting to the byte-identical ciphertext is conclusive."""
    ct = letters(CT_PATH.read_text())
    assert encrypt(decrypt(ct)) == ct


def test_primer_is_the_first_five_ciphertext_letters():
    """Why the challenge is solvable at all: the plaintext opens with a yelled
    AAAAA, and A adds nothing, so ct[0:5] IS the primer, printed on line 1."""
    ct = letters(CT_PATH.read_text())
    assert ct[:5] == PRIMER


def test_wrong_primer_does_not_yield_the_flag():
    """Guards against a solve that works for the wrong reason."""
    ct = letters(CT_PATH.read_text())
    assert "down_with_cis_bus" not in find_flag(decrypt(ct, primer="aaaaa"))


# --------------------------------------------------------------------------
# Characterisation — the recon phase
# --------------------------------------------------------------------------


def _stream_without_cribs():
    text = CT_PATH.read_text()
    return letters(re.sub(r"\b[A-Z]{3,}\b", "", text))


def _ic(s):
    n = len(s)
    return sum(v * (v - 1) for v in Counter(s).values()) / (n * (n - 1)) if n > 1 else 0


def _avg_column_ic(s, k):
    return sum(_ic(s[i::k]) for i in range(k)) / k


def test_index_of_coincidence_stays_flat():
    """Why classical Vigenere analysis found nothing: an autokey has no period
    at all, so no column split ever aligns. Correct signal, and it pointed at
    the right family (running key) — an autokey IS a running key whose key
    text happens to be the message itself."""
    s = _stream_without_cribs()
    scores = {k: _avg_column_ic(s, k) for k in range(1, 16)}
    assert all(v < (ENGLISH_IC + RANDOM_IC) / 2 for v in scores.values()), scores


def test_caps_words_are_the_five_plaintext_letters_before_them():
    """The ALL-CAPS words are the ciphertext of the yelled AAAAA. Since
    A contributes a zero shift, each one is the raw key at that position —
    and the key is the plaintext delayed by five. So every caps word is
    literally the five plaintext letters that precede it."""
    pt = decrypt(letters(CT_PATH.read_text()))
    text = CT_PATH.read_text()

    pos, checked = 0, 0
    for tok in re.findall(r"[A-Za-z]+", text):
        if tok.isupper() and len(tok) >= 3:
            # The yell occupies 5 plaintext letters starting here.
            assert pt[pos : pos + 5] == "aaaaa", (tok, pos, pt[pos : pos + 5])
            if pos >= 5:
                assert tok.lower()[:5] == pt[pos - 5 : pos], tok
                checked += 1
        pos += len(tok)
    assert checked >= 8, f"only checked {checked} cribs"


def test_shirt_and_flag_share_two_words():
    """The near-identical runs at 202 and 342 that looked like a repeating
    key: 'down with cis' on the shirt and 'down_with_cis' in the flag are the
    same words, so their key streams agree wherever the preceding five
    plaintext letters agree. Structure in the plaintext, not the key."""
    pt = decrypt(letters(CT_PATH.read_text()))
    assert pt.count("downwithcis") == 2


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
