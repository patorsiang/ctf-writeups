"""Tests for EVEN RSA CAN BE BROKEN???.

Three kinds live here, deliberately:

  * Correctness against the real capture — proves the pinned (N, e, c)
    from the live instance actually decrypts to the real flag.
  * A known-bad case for factor_even_modulus — an oracle that only ever
    says "yes, exploitable" isn't the same as one that correctly says
    "no" when the modulus doesn't have this specific bug.
  * A full round trip against a freshly, independently generated
    vulnerable key (using a from-scratch Miller-Rabin prime generator,
    not the pinned capture), proving the *attack*, not just this one N.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import random

from solve import CAPTURED_C, CAPTURED_E, CAPTURED_N, decrypt, factor_even_modulus

FLAG = b"picoCTF{tw0_1$_pr!m31c9046c4}"


# --------------------------------------------------------------------------
# Correctness against the real capture
# --------------------------------------------------------------------------


def test_decrypts_the_captured_instance_to_the_real_flag():
    assert decrypt(CAPTURED_N, CAPTURED_E, CAPTURED_C) == FLAG


def test_captured_modulus_is_even():
    """Why the attack applies at all: N's parity alone reveals p = 2,
    with no factoring algorithm needed."""
    assert CAPTURED_N % 2 == 0


# --------------------------------------------------------------------------
# Known-bad case for the factoring oracle
# --------------------------------------------------------------------------


def test_rejects_an_odd_modulus():
    """A modulus without this specific bug must be rejected, not
    silently mis-factored into a bogus (p, q). Guards against an oracle
    that was only ever tested on cases where the answer is yes."""
    odd_N = 15  # 3 * 5, both odd -- not the vulnerability this targets
    try:
        factor_even_modulus(odd_N)
        assert False, "expected ValueError for an odd modulus"
    except ValueError:
        pass


# --------------------------------------------------------------------------
# The attack itself, against a fresh synthetic key
# --------------------------------------------------------------------------


def _is_probable_prime(n, rounds=20):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_prime(bits):
    while True:
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate):
            return candidate


def _make_vulnerable_key(bits=512):
    """Reproduces encrypt.py's gen_key, standing in for the undisclosed
    setup.get_primes() bug: one "prime" always comes out as 2."""
    p = 2
    q = _random_prime(bits)
    N = p * q
    e = 65537
    d = pow(e, -1, (p - 1) * (q - 1))
    return N, e, d


def test_attack_recovers_an_arbitrary_message_from_a_fresh_vulnerable_key():
    """The real proof: generate a brand-new key with the same structural
    bug (independent of the pinned capture) and confirm the attack
    recovers an arbitrary message end to end -- encrypt, then decrypt
    using only (N, e, c), never the freshly generated d."""
    N, e, _d = _make_vulnerable_key()
    message = b"testing_1_2_3"
    m_int = int.from_bytes(message, "big")
    c = pow(m_int, e, N)

    assert decrypt(N, e, c) == message


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
