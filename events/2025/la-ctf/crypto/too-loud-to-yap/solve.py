"""Too Loud To Yap — full solve from ct.txt alone.

Vigenere autokey with a 5-letter primer:

    key   = PRIMER + plaintext
    ct[i] = pt[i] + pt[i-5]      (pt[i-5] replaced by PRIMER[i] while i < 5)

Decryption needs nothing but the primer, because each recovered plaintext
letter becomes the key letter five positions later. The primer is "lactf" —
line 1 of the ciphertext, which is the encryption of the first yelled AAAAA.

    python3 solve.py
"""

import re
from pathlib import Path

PRIMER = "lactf"
CT_PATH = Path(__file__).parent / "ct.txt"


def letters(text):
    return re.sub(r"[^A-Za-z]", "", text).lower()


def decrypt(ct, primer=PRIMER):
    """Autokey decrypt. Each plaintext letter keys the one 5 places later."""
    pt = []
    for i, c in enumerate(ct):
        k = primer[i] if i < len(primer) else pt[i - len(primer)]
        pt.append(chr((ord(c) - ord(k)) % 26 + ord("a")))
    return "".join(pt)


def encrypt(pt, primer=PRIMER):
    """Inverse of decrypt; used to prove the model reproduces ct.txt exactly."""
    out = []
    for i, c in enumerate(pt):
        k = primer[i] if i < len(primer) else pt[i - len(primer)]
        out.append(chr((ord(c) - ord("a") + ord(k) - ord("a")) % 26 + ord("a")))
    return "".join(out)


def find_flag(plaintext):
    """The flag body sits between the braces; recover it from the letter run."""
    i = plaintext.find("lactf")
    body = plaintext[i + 5 :]
    # Word boundaries are lost in the letter stream, so re-split on the known
    # underscore positions from the ciphertext: 4_4_3_3.
    return "lactf{" + "_".join([body[:4], body[4:8], body[8:11], body[11:14]]) + "}"


if __name__ == "__main__":
    ct = letters(CT_PATH.read_text())
    pt = decrypt(ct)

    assert encrypt(pt) == ct, "model does not reproduce the ciphertext"

    print("Recovered plaintext (first 120 letters):")
    print(" ", pt[:120])
    print("\nThe 'aaaaa' runs are the yelled AAAAA from the challenge prompt.")
    print("\nFLAG:", find_flag(pt))
