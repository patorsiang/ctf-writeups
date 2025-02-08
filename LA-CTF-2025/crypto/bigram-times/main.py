from itertools import product

# Given character set
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
char_map = {c: i + 1 for i, c in enumerate(characters)}  # Mapping character to index
reverse_map = {i + 1: c for i, c in enumerate(characters)}  # Reverse mapping index to character

# Encrypted flag from the challenge
shifted_flag = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"

# Define the decryption function
def inverse_bigram_multiplicative_shift(enc_bigram):
    """Given an encrypted bigram, return all possible original bigrams."""
    pos1_enc = char_map[enc_bigram[0]]
    pos2_enc = char_map[enc_bigram[1]]

    possible_bigrams = []

    # Try all possible original characters
    for p1, p2 in product(characters, repeat=2):
        pos1 = char_map[p1]
        pos2 = char_map[p2]

        shift = (pos1 * pos2) % 67

        if ((pos1 * shift) % 67) == pos1_enc and ((pos2 * shift) % 67) == pos2_enc:
            possible_bigrams.append(p1 + p2)

    return possible_bigrams

# Decrypt the flag
possible_flags = [""]

for i in range(0, len(shifted_flag), 2):
    enc_bigram = shifted_flag[i:i+2]
    possible_bigrams = inverse_bigram_multiplicative_shift(enc_bigram)

    new_flags = []
    for partial_flag in possible_flags:
        for bigram in possible_bigrams:
            new_flags.append(partial_flag + bigram)

    possible_flags = new_flags

# Print possible flag candidates
for flag in possible_flags:
    if flag.startswith("lactf{"):
        print("[+] Possible Flag:", flag)
