# Big E

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Unknown
- Status: Solved
- Files: [chall.py](chall.py)
- Skills Learned: RSA common modulus attack, extended Euclidean algorithm

## Problem Summary

The challenge gives two RSA ciphertexts encrypted under the same modulus with different public exponents.

## What I Tried

Record the two ciphertexts, the shared modulus, and the two public exponents. Check whether the exponents are coprime.

## Key Idea

If two RSA ciphertexts use the same plaintext and modulus with coprime exponents, Bezout coefficients can combine them to recover the plaintext.

## Solution Walkthrough

Use the extended Euclidean algorithm to find `a` and `b` such that `a * e1 + b * e2 = 1`. If either coefficient is negative, invert that ciphertext modulo `n`. Then compute:

```python
pt = pow(ct_1, a, n) * pow(ct_2, b, n) % n
```

Convert the resulting integer back to bytes.

## Flag

`lactf{b1g_3_but_sm4ll_d!!!_part2_since_i_trolled}`

## Lessons Learned

- Reusing an RSA modulus across related messages is dangerous.
- The extended Euclidean algorithm is a practical crypto tool, not just theory.
