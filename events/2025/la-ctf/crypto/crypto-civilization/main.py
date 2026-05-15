import hashlib
import os
import socket
import binascii

# PRG function (same as in challenge)
def PRG(s: bytes) -> bytes:
    assert len(s) == 2, "Invalid input size!"
    h = hashlib.new("sha3_256")
    h.update(s)
    out = h.digest()
    return out[:4]  # 4-byte output

# XOR function
def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

# Precompute PRG values for all 2-byte `s` values
prg_lookup = {}
for i in range(65536):
    s = i.to_bytes(2, byteorder="big")
    prg_lookup[PRG(s)] = s

# Connect to challenge server
HOST = "chall.lac.tf"
PORT = 31173

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.recv(1024)  # Skip intro messages

correct_answers = 0

for _ in range(200):
    s.recv(1024)  # "Crypto test #X"
    y_line = s.recv(1024).decode()  # "Here's y: <hex>"
    y_hex = y_line.split(": ")[1].strip()
    y = binascii.unhexlify(y_hex)

    s.recv(1024)  # "What's your commitment?"
    com = os.urandom(4)  # Pick a random commitment
    s.sendall(binascii.hexlify(com) + b"\n")

    response = s.recv(1024).decode()

    if "commit the chicken" in response:
        # The server expects PRG(s) = com
        s.sendall(binascii.hexlify(prg_lookup[com]) + b"\n")

    elif "commit the beef" in response:
        # The server expects PRG(s) XOR y = com
        target = xor_bytes(com, y)
        s.sendall(binascii.hexlify(prg_lookup[target]) + b"\n")

    # Check response
    final_response = s.recv(1024).decode()
    if "Good work" in final_response:
        correct_answers += 1

# Print the flag if we pass at least 133 rounds
if correct_answers >= 133:
    print(s.recv(1024).decode())  # Should print the flag

s.close()
