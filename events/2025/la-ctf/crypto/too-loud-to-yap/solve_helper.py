"""Tools for attacking a running-key cipher. No flag inside — you drive it.

The defining property of a running key: BOTH the plaintext and the key are
English. That is also the weakness. For any ciphertext segment, only a few
(plaintext, key) word pairs exist where both halves are real words.

    python3 solve_helper.py            # demo on a known-solved segment
"""

import re
from pathlib import Path

HERE = Path(__file__).parent
A = ord("a")


def stream():
    """Ciphertext as one letter run, ALL-CAPS crib words removed."""
    text = (HERE / "ct.txt").read_text()
    out = []
    for tok in re.findall(r"[A-Za-z]+", text):
        if tok.isupper() and len(tok) >= 3:
            continue
        out.extend(tok.lower())
    return "".join(out)


def cribs():
    """(position_in_stream, crib_text) for each ALL-CAPS word."""
    text = (HERE / "ct.txt").read_text()
    pos, found = 0, []
    for tok in re.findall(r"[A-Za-z]+", text):
        if tok.isupper() and len(tok) >= 3:
            found.append((pos, tok.lower()))
        else:
            pos += len(tok)
    return found


def subtract(ct, pt):
    """key = ct - pt (mod 26)"""
    return "".join(chr((ord(c) - ord(p)) % 26 + A) for c, p in zip(ct.lower(), pt.lower()))


def decrypt(ct, key):
    """pt = ct - key (mod 26). Same operation; named for intent."""
    return subtract(ct, key)


def encrypt(pt, key):
    """ct = pt + key (mod 26). Only used to build test fixtures."""
    return "".join(chr((ord(p) + ord(k) - 2 * A) % 26 + A) for p, k in zip(pt, key))


# The shirt phrase (line 7) and the flag body (line 9) share two words.
SHIRT_POS, FLAG_POS, SHARED_LEN = 202, 342, 7  # "?lhd pea" in both places


def segments_agree(ct_a, key_a, ct_b, key_b):
    """Candidate-key oracle: do two ciphertext runs decrypt to the same text?

    NECESSARY, NOT SUFFICIENT. Agreement means a key pair survives; it does not
    mean the key is right — see test_oracle_admits_false_positives. Use it to
    reject candidates, never to declare victory.
    """
    return decrypt(ct_a, key_a) == decrypt(ct_b, key_b)


def load_words(min_len=1):
    path = Path("/usr/share/dict/words")
    return {
        w.strip().lower()
        for w in path.read_text().splitlines()
        if len(w.strip()) >= min_len and w.strip().isalpha()
    }


def word_pairs(ct_segment, words):
    """Every (plaintext, key) pair of real words that produces this ciphertext.

    WARNING — weak here, and the reason is worth understanding. This requires a
    key word to line up exactly with a plaintext word. The recovered key
    fragments show that does not happen: 'hewas' is "he was", 'overy' is
    "o very", 'ngout' is "ng out". Running prose ignores plaintext word
    boundaries, so the true pair is usually absent from the results while
    twenty coincidental pairs are present. Use drag() instead.
    """
    n = len(ct_segment)
    hits = []
    for pt in (w for w in words if len(w) == n):
        key = subtract(ct_segment, pt)
        if key in words:
            hits.append((pt, key))
    return sorted(hits)


def drag(word, ct=None, top=None):
    """Slide a candidate key word along the ciphertext, showing what falls out.

    Use when you have a guess about a word in the KEY text but not where it sits.
    """
    ct = ct or stream()
    n = len(word)
    return [(i, decrypt(ct[i : i + n], word)) for i in range(len(ct) - n + 1)][:top]


if __name__ == "__main__":
    s = stream()
    print(f"stream: {len(s)} letters")
    print(f"flag ciphertext begins at index {s.find('lactf') + 5}\n")

    print("Known crib windows (ciphertext immediately before each CAPS word):")
    for pos, crib in cribs():
        ct = s[pos - len(crib) : pos]
        if ct:
            print(f"  {pos - len(crib):4d}  {ct:8s} - {crib:8s} = {subtract(ct, crib)}")

    flag_ct = s[s.find("lactf") + 5 :][:14]
    print(f"\nflag ciphertext: {flag_ct}  (groups: 4_4_3_3)")

    print("\nUnencrypted stretches (key = 'aaaaa' there):")
    print(f"  {s[:15]!r} at 0, and the {'lactf'!r} wrapper at 333")
    print("\nUse drag(word) with candidate KEY fragments, or subtract() with")
    print("candidate PLAINTEXT. Both halves must read as English.")
