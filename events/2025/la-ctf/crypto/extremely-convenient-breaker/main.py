import socket
import re

# Challenge server details
HOST = "chall.lac.tf"
PORT = 31180

# Function to connect and receive initial data
def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    data = s.recv(4096).decode()

    # Extract encrypted flag using regex
    match = re.search(r"Here's the encrypted flag in hex:\s*([\da-f]+)", data)
    if not match:
        print("[-] Failed to retrieve the encrypted flag!")
        s.close()
        return None, None

    encrypted_flag = match.group(1)
    print(f"[+] Encrypted Flag: {encrypted_flag}")

    return s, encrypted_flag

# Function to send ciphertext and get decrypted response
def query_oracle(s, ciphertext):
    s.sendall(ciphertext.encode() + b"\n")
    response = s.recv(4096).decode()
    return response.strip()

# Connect and retrieve encrypted flag
s, enc_flag_hex = connect_to_server()
if s is None:
    exit()

# Split encrypted flag into 16-byte (32 hex char) blocks
enc_blocks = [enc_flag_hex[i:i+32] for i in range(0, len(enc_flag_hex), 32)]

# Decrypt each block by submitting it 4 times
plaintext_blocks = []
for i, block in enumerate(enc_blocks):
    modified_ciphertext = block * 4  # Repeat block 4 times
    response = query_oracle(s, modified_ciphertext)
    print(f"Decrypted Block {i+1}: {response}")
    plaintext_blocks.append(response)

# Close the connection
s.close()

# Reassemble the flag
flag = "".join(plaintext_blocks)
print(f"[+] Recovered Flag: {flag}")
