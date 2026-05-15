# RSAaaS

## Metadata

- Event: LA CTF 2025
- Category: Crypto
- Difficulty: Unknown
- Status: Solved
- Files: [chall.py](chall.py), [main.py](main.py)
- Skills Learned: RSA key validation, Euler phi, greatest common divisor

## Problem Summary

The service asks for RSA parameters. The weakness is in whether the generated parameters are actually valid for the chosen public exponent.

## What I Tried

Generate nearby primes and inspect whether `gcd(phi, e)` is valid for RSA decryption.

## Key Idea

RSA requires `gcd(phi, e) = 1`. Supplying parameters where that condition fails breaks the expected RSA setup.

## Solution Walkthrough

The solve approach in [main.py](main.py) searches for primes where `gcd((p - 1) * (q - 1), 65537) != 1`, then uses those values against the service.

## Flag

`lactf{actually_though_whens_the_last_time_someone_checked_for_that}`

## Lessons Learned

- RSA implementations must validate mathematical preconditions, not only input size.
