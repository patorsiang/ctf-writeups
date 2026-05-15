from sympy import nextprime, gcd

e = 65537

# Start with a valid large prime
p = nextprime(2**63)
q = nextprime(p + 100000)  # Pick another nearby prime

phi = (p - 1) * (q - 1)

# Ensure gcd(phi, e) ≠ 1
while gcd(phi, e) == 1:
    q = nextprime(q + 100000)  # Keep adjusting q
    phi = (p - 1) * (q - 1)

print(f"p = {p}, q = {q}")
print(f"gcd(phi, e) = {gcd(phi, e)} (Should NOT be 1)")
