"""Bigram Times — full solve from the values printed by chall.py.

The cipher treats each plaintext bigram (a, b) as two nonzero elements of
Z/67Z (67 is prime, and the 66-character alphabet maps onto 1..66 = the
nonzero residues) and computes:

    shift = a * b            (mod 67)
    a'    = a * shift  =  a^2 * b
    b'    = b * shift  =  a * b^2

This is a *cubic* map: a' * b' = (a*b)^3 (mod 67). Since gcd(3, 66) = 3,
cubing on this group is 3-to-1, so every ciphertext bigram has exactly
three valid plaintext preimages — the cipher is deliberately not
injective. chall.py hands you two of the three as decoys
(`not_the_flag`, `also_not_the_flag`); the real flag is whichever
preimage isn't one of those two, at every position.

    python3 solve.py
"""

from pathlib import Path

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
MOD = 67

POS = {c: i + 1 for i, c in enumerate(CHARACTERS)}
CHAR = {i + 1: c for i, c in enumerate(CHARACTERS)}

# Printed by chall.py.
SHIFTED_FLAG = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
NOT_THE_FLAG = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
ALSO_NOT_THE_FLAG = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"


def encrypt_bigram(bigram):
    """chall.py's bigram_multiplicative_shift, reproduced for verification."""
    a, b = POS[bigram[0]], POS[bigram[1]]
    shift = (a * b) % MOD
    return CHAR[(a * shift) % MOD] + CHAR[(b * shift) % MOD]


def build_reverse_table():
    """Every ciphertext bigram <- all plaintext bigrams that encrypt to it.

    Brute force over the 66x66 domain (4356 pairs) done once, up front —
    not per ciphertext bigram, and never combined across positions. That
    combinatorial product (3 candidates ^ 24 positions) is what makes the
    naive brute-force solve in main.py blow up.
    """
    table = {}
    for a in CHARACTERS:
        for b in CHARACTERS:
            table.setdefault(encrypt_bigram(a + b), []).append(a + b)
    return table


def solve(shifted_flag, not_the_flag, also_not_the_flag, table=None):
    table = table or build_reverse_table()
    decoys = (not_the_flag, also_not_the_flag)
    flag = []
    for i in range(0, len(shifted_flag), 2):
        candidates = table[shifted_flag[i : i + 2]]
        real = [c for c in candidates if c not in (d[i : i + 2] for d in decoys)]
        assert len(real) == 1, (i, candidates)
        flag.append(real[0])
    return "".join(flag)


if __name__ == "__main__":
    table = build_reverse_table()
    flag = solve(SHIFTED_FLAG, NOT_THE_FLAG, ALSO_NOT_THE_FLAG, table)

    reconstructed = "".join(encrypt_bigram(flag[i : i + 2]) for i in range(0, len(flag), 2))
    assert reconstructed == SHIFTED_FLAG, "model does not reproduce the ciphertext"

    print("FLAG:", flag)
