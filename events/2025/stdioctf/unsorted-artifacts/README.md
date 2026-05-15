# STDiOCTF 2025 Notebook Writeups

## Metadata

- Event: STDiOCTF 2025
- Category: Mixed
- Difficulty: Mixed
- Status: In progress
- Main Writeup: [main.ipynb](main.ipynb)
- Files: [main.ipynb](main.ipynb), [Archive.zip](Archive.zip)
- Skills Learned: Cloud storage versioning, RSA oracle attacks, mobile log inspection, reverse engineering

# STDiOCTF-2025

## Misc

### Sanity Check

Welcome to STDiO CTF 2025!
Before jumping into the real hacking challenges, let’s make sure everything is working correctly.

Your task is simple, the flag is split into 2 sections. You must collect both pieces (one from Discord found in the #stdio2025-announcement channel, one from the spawned challenge machine) and combine them to form the final flag.

🔗 Join US : https://discord.gg/SeXD7syx

🏁 Flag Format

STDIO2025_xx{}

flag: `STDIO2025_00{Welcome_To_STDiO_CTF_2025_e28a0baaef3c}`

### CLOUD 🍰 Ghost in the Bucket

A junior developer ran a deployment script to a GCP bucket hosting a static website. On their first deployment, they accidentally pushed sensitive files. They immediately deployed a new version with all sensitive files removed. Is everything OK?

https://ghost-in-the-bucket.storage.googleapis.com/

**Solution**

```bash
curl -s 'https://ghost-in-the-bucket.storage.googleapis.com/?versions' \
  | grep -Eo '<Key>[^<]+</Key>|<Generation>[0-9]+</Generation>' \
  | sed 'N;s/\n/ /'

# <Key>404.html</Key> <Generation>1762578815878180</Generation>
# <Key>config.js</Key> <Generation>1762578809508193</Generation>
# <Key>config.js</Key> <Generation>1762578815928633</Generation>
# <Key>index.html</Key> <Generation>1762578809513421</Generation>
# <Key>index.html</Key> <Generation>1762578815884901</Generation>
# <Key>styles.css</Key> <Generation>1762578815932452</Generation>

curl -s 'https://storage.googleapis.com/ghost-in-the-bucket/config.js?generation=1762578809508193' -o config.old.js
```

flag: `STDIO2025_35{833fb6d5371ee0c0eb46bcdee4a6f2be}`

## Crypto

### Oracle of Evenness

Interact with an RSA oracle that encrypts and decrypts messages. It refuses to reveal the flag directly — subtle differences in responses are your only clues.

Author: boomoioi

```python
#!/usr/bin/env python3
# exploit_nopwn.py
# Connects to challenge.stdio.2600.in.th:30675 and performs the multiplicative RSA oracle attack
# Requires: Python 3.8+ (for pow(..., -1, n) inverse)

import socket
import sys
from math import gcd

HOST = "challenge.stdio.2600.in.th"
PORT = 30239
RECV_BUF = 4096
TIMEOUT = 5.0

def recv_until(sock: socket.socket, marker: bytes = b">>> "):
    """Receive until marker is seen (or timeout). Returns bytes."""
    sock.settimeout(TIMEOUT)
    data = b""
    try:
        while marker not in data:
            chunk = sock.recv(RECV_BUF)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data

def send_line(sock: socket.socket, s: str):
    sock.sendall((s + "\n").encode())

def parse_info_block(data: bytes):
    """Find FLAG_CIPHERTEXT_HEX, N and e in the text and return them."""
    text = data.decode(errors="ignore")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    C_hex = None
    N = None
    e = None
    for L in lines:
        if L.startswith("FLAG_CIPHERTEXT_HEX"):
            # formats like: FLAG_CIPHERTEXT_HEX = 0xdeadbeef...
            parts = L.split("=", 1)
            if len(parts) > 1:
                C_hex = parts[1].strip()
                # optional: remove surrounding quotes
                if C_hex.startswith(("'", '"')) and C_hex.endswith(("'", '"')):
                    C_hex = C_hex[1:-1]
        elif L.startswith("N"):
            parts = L.split("=", 1)
            if len(parts) > 1:
                try:
                    N = int(parts[1].strip())
                except ValueError:
                    # maybe hex
                    N = int(parts[1].strip(), 0)
        elif L.startswith("e"):
            parts = L.split("=", 1)
            if len(parts) > 1:
                e = int(parts[1].strip())
    return C_hex, N, e

def parse_decrypted_integer(data: bytes):
    text = data.decode(errors="ignore")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Decrypted integer:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                try:
                    return int(parts[1].strip())
                except ValueError:
                    pass
        # fallback: some servers print "Integer: 12345" or similar
        if line.lower().startswith("integer:"):
            try:
                return int(line.split(":",1)[1].strip())
            except Exception:
                pass
    return None

def int_to_bytes(m: int):
    if m == 0:
        return b"\x00"
    blen = (m.bit_length() + 7) // 8
    return m.to_bytes(blen, "big")

def main():
    print(f"[+] connecting to {HOST}:{PORT} ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # read initial banner / prompt
    banner = recv_until(sock)
    print("[<] initial banner:")
    print(banner.decode(errors="ignore"))

    # request info
    print("[+] sending: info")
    send_line(sock, "info")
    info_resp = recv_until(sock)
    print("[<] info response:")
    print(info_resp.decode(errors="ignore"))

    C_hex, N, e = parse_info_block(info_resp)
    if not (C_hex and N and e):
        print("[-] couldn't parse FLAG_CIPHERTEXT_HEX, N or e from server response")
        sock.close()
        sys.exit(1)

    # Normalize C_hex (strip 0x if present)
    if C_hex.startswith("0x") or C_hex.startswith("0X"):
        C_hex_clean = C_hex[2:]
    else:
        C_hex_clean = C_hex
    C = int(C_hex_clean, 16)

    print(f"[+] parsed C (hex): 0x{C:x}")
    print(f"[+] parsed N: {N}")
    print(f"[+] parsed e: {e}")

    # pick k
    for candidate_k in (2, 3, 5, 7, 11, 13, 17):
        if gcd(candidate_k, N) == 1:
            k = candidate_k
            break
    else:
        print("[-] couldn't find small k coprime to N; try larger k manually")
        sock.close()
        sys.exit(1)

    print(f"[+] chosen k = {k} (gcd(k,N) == 1)")

    # compute C' = C * k^e mod N
    ke = pow(k, e, N)
    Cp = (C * ke) % N
    Cp_hex = hex(Cp)[2:]
    print(f"[+] crafted C' (hex): 0x{Cp:x}")

    # ask server to decrypt C'
    cmd = f"decrypt {Cp_hex}"
    print(f"[+] sending: {cmd}")
    send_line(sock, cmd)

    dec_resp = recv_until(sock)
    print("[<] decrypt response:")
    print(dec_resp.decode(errors="ignore"))

    mp = parse_decrypted_integer(dec_resp)
    if mp is None:
        print("[-] couldn't find 'Decrypted integer' in response.")
        # print raw and exit
        sock.close()
        sys.exit(1)

    print(f"[+] got m' = {mp}")

    # compute k^{-1} mod N and recover m
    try:
        kinv = pow(k, -1, N)
    except ValueError:
        print("[-] modular inverse failed (k not invertible).")
        sock.close()
        sys.exit(1)

    m = (mp * kinv) % N
    print(f"[+] recovered m (int): {m}")

    m_bytes = int_to_bytes(m)
    print("[+] recovered bytes (maybe UTF-8):")
    try:
        decoded = m_bytes.decode("utf-8")
        print(decoded)
    except UnicodeDecodeError:
        print(m_bytes)
        # also show hex
        print("hex:", m_bytes.hex())

    print("[+] done.")
    sock.close()

if __name__ == "__main__":
    main()
```

flag: `STDIO2025_09{OrACI3_PAr1tY_817_47taCK_94b47eeb9237}`

### 🔥 Divine Oracle

As you succeed, the divine has fixed its gaze upon you, watching to see how you will carry the weight of destiny.

**Solution**

- `nc challenge.stdio.2600.in.th 30869`

```python
import re
import random
import socket

HOST = "challenge.stdio.2600.in.th"
PORT = 31477

while True:
    try:
        s = socket.create_connection((HOST, PORT))
        for i in range(64):
            print(f"\n==== Seeker {i} ====")
            b = random.randint(0, 1)
            print(f"b: {b}")
            data = recv_until(s, b"v:")
            print(data)

            n  = parse_int(b"n",  data)
            e  = parse_int(b"e",  data)
            x0 = parse_int(b"x0", data)
            x1 = parse_int(b"x1", data)

            print(f"n: {n}")
            print(f"e: {e}")
            print(f"x0: {x0}")
            print(f"x1: {x1}")

            # Compute v for chosen side
            xb = x0 if b == 0 else x1
            v = (xb + pow(r, e, n)) % n

            print(f"v: {v}")
            s.sendall(str(v).encode() + b"\n")

            # Get c0/c1, then it prints: "Oracle: This is your fate" and a prompt '>\s'
            data = recv_until(s, b"Oracle: This is your fate")

            c0 = parse_int(b"c0", data)
            c1 = parse_int(b"c1", data)

            print(f"c0: {c0}")
            print(f"c1: {c1}")

            cb = c0 if b == 0 else c1
            mb = (cb - r) % n
            m_bytes = mb.to_bytes((mb.bit_length() + 7)//8, "big")
            msg = m_bytes.decode(errors="replace")
            m_fate = re.search(r"Oracle \(reveals ([^)]+)\):\s*(.+?)[.?!]\s", msg)
            m_flavor = re.search(r"flavor\s+(\d+)", msg)

            title = m_fate.group(1).strip()
            text  = m_fate.group(2).strip()
            if not text.endswith("."):
                text += "."

            answer = f"{title}: {text}"
            print(f"✅ Fate (answer): {answer}")
            s.sendall((answer + "\n").encode())

            flavor = m_flavor.group(1)
            print(f"✅ Flavor: {flavor}")
            s.sendall((flavor + "\n").encode())
    except Exception as ex:
        print(f"❌ Error: {ex}")
        continue
```

```python
import re
import socket

HOST = "challenge.stdio.2600.in.th"
PORT = 31477

# --- helpers ---------------------------------------------------------------

def recv_until(s, token: bytes, max_bytes=1_000_000):
    buf = bytearray()
    while token not in buf:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
        if len(buf) > max_bytes:
            break
    return bytes(buf)

def parse_int(key: bytes, data: bytes) -> int:
    # finds lines like: b"n: 12345" (spaces tolerant)
    pat = re.compile(rb"\b" + re.escape(key) + rb"\s*:\s*([0-9]+)")
    m = pat.search(data)
    if not m:
        raise ValueError(f"Cannot find integer for {key!r}")
    return int(m.group(1))

_fate_re = re.compile(
    r"Oracle\s*\(reveals\s*([^)]+)\):\s*([\s\S]*?)(?:\s*(?:The\s+divine\s+flavo[u]?r\b)|\Z)",
    re.IGNORECASE,
)
_flavor_re = re.compile(r"(?i)\bflavo[u]?r\b\s*[:=]?\s*(\d+)")

def parse_answer_and_flavor(msg: str):
    # Extract title + description and the flavor (if present)
    m_fate = _fate_re.search(msg)
    if not m_fate:
        return None, None
    title = m_fate.group(1).strip()
    desc = m_fate.group(2).strip().replace("\r", " ").replace("\n", " ")
    # normalize single trailing punctuation
    if not desc.endswith("."):
        desc += "."
    answer = f"{title}: {desc}"

    m_flavor = _flavor_re.search(msg)
    flavor = m_flavor.group(1) if m_flavor else None
    return answer, flavor

def to_text(mb: int) -> str:
    if mb == 0:
        return ""
    m_bytes = mb.to_bytes((mb.bit_length() + 7)//8, "big")
    return m_bytes.decode(errors="replace")

# --- main solve loop -------------------------------------------------------

def solve():
    successes = 0
    b_guess = 0        # we’ll flip this only when we detect a fake
    r = 2              # fixed small r
    print("Starting… need 64 correct fates.\n")

    while successes < 64:
        try:
            s = socket.create_connection((HOST, PORT), timeout=8)
            s.settimeout(8)

            # Wait for a seeker block up to the "v:" prompt
            banner = recv_until(s, b"v:")
            # parse params
            n  = parse_int(b"n",  banner)
            e  = parse_int(b"e",  banner)
            x0 = parse_int(b"x0", banner)
            x1 = parse_int(b"x1", banner)

            xb = x0 if b_guess == 0 else x1
            v  = (xb + pow(r, e, n)) % n
            s.sendall(str(v).encode() + b"\n")

            # Receive c0/c1 and the fate header
            data = recv_until(s, b"Oracle: This is your fate")
            c0 = parse_int(b"c0", data)
            c1 = parse_int(b"c1", data)

            cb = c0 if b_guess == 0 else c1
            mb = (cb - r) % n
            msg = to_text(mb)

            answer, flavor = parse_answer_and_flavor(msg)

            if not flavor:
                # This was the fake. Flip side, close, try again without incrementing successes.
                print(f"[fake] b={b_guess} had no flavor. Flipping b and retrying…")
                b_guess ^= 1
                s.close()
                continue

            # We have the real fate; send exact answer then flavor
            print(f"[real] seeker #{successes} b={b_guess}")
            print(f"  answer: {answer}")
            print(f"  flavor: {flavor}")

            # The service prints a '>' prompt before each input. Read until '>' then send.
            recv_until(s, b">")
            s.sendall((answer + "\n").encode())
            recv_until(s, b">")
            s.sendall((flavor + "\n").encode())

            # Read the server’s acknowledgement for this seeker
            ack = s.recv(4096)  # best-effort
            # If it contains a failure line, we’ll just loop and try again; otherwise count success
            if b"murmur" in ack or b"uncertain" in ack:
                print("  server rejected unexpectedly; retrying seeker (keep b).")
                s.close()
                continue

            successes += 1
            print(f"  ✓ success {successes}/64\n")

            # keep same b_guess on success (do NOT flip)

            # if we happen to still have the same TCP session, it will prompt the next seeker;
            # otherwise next loop will reconnect as needed.

            s.close()

        except Exception as ex:
            print(f"[io] {type(ex).__name__}: {ex}; reconnecting…")
            try:
                s.close()
            except:
                pass
            continue

    print("\nAll 64 done. The service should have printed the sacred token / flag near the end.")

if __name__ == "__main__":
    solve()
```

## Mobile

### looooooooo(n)g cat

Think like the developer — the app quietly reveals things while it runs. Look for something out of place in its runtime chatter

Author: decl, boomoioi

**Solution**

- download apk
- open android emulator
- install it
- look the log

```bash
adb devices # should show: emulator-5554    device

adb install -r -g cat.apk
adb shell am start -n stdio.cat/.MainActivity
adb logcat -s STDIO_FLAG
```

flag: `STDIO2025_44{186925c99f5871ce4883c09e0a2819e0591d57ada56acb28d74f5da4d9d727b8}`

## Reverse

### Golden Ticket

GCC is not opened for the registration yet but you know how to get the ticket before others...

Instruction: Get file from the server then reverse it. The flag is not on the server - no need to pentest it.

⚠️ This challenge allows only 10 tries of flag submission. Do NOT brute force or guess it.

Author: Bankde

flag: `STDIO2025_18{rOAd_7O_Gcc20zG_WlTH_6o1d3N_7ICket_03117e97b5c4}`

```python
# Cell 1 — configuration & quick file-check
from pathlib import Path
JS_PATH = Path("gcc2026-challenge/decryptFlag.js")   # change if needed
KNOWN_PREFIX = b"STDIO2025_"

if not JS_PATH.exists():
    raise FileNotFoundError(f"File not found: {JS_PATH.resolve()}")
print("Known prefix:", KNOWN_PREFIX)

# Cell 2 — extract the hex byte array from the JS file
import re
txt = JS_PATH.read_text(encoding="utf-8", errors="ignore")

# find the Uint8Array([...]) block
m = re.search(r"Uint8Array\s*\(\s*\[\s*([^\]]+)\]\s*\)", txt, flags=re.S)
if not m:
    # fallback: first bracketed array
    m = re.search(r"\[\s*(0x[0-9A-Fa-f,xX\s]+)\s*\]", txt)
if not m:
    raise ValueError("Couldn't find Uint8Array(...) in the JS file. Paste a snippet if this fails.")

arr_text = m.group(1)
# extract hex or decimal tokens
tokens = re.findall(r"0x[0-9A-Fa-f]+|\d+", arr_text)
bytes_list = []
for t in tokens:
    if t.startswith(("0x","0X")):
        bytes_list.append(int(t,16) & 0xFF)
    else:
        bytes_list.append(int(t) & 0xFF)

cipher = bytes(bytes_list)
print("Extracted cipher bytes:", len(cipher))
print("First 32 bytes (hex):", cipher[:32].hex())

# Cell 3 — derive repeating 4-byte key from known prefix and decrypt
from textwrap import shorten

if len(cipher) < len(KNOWN_PREFIX):
    raise ValueError("Cipher is shorter than the known prefix; can't do known-plaintext attack.")

# derive bytewise from the known prefix
derived = bytearray(cipher[i] ^ KNOWN_PREFIX[i] for i in range(len(KNOWN_PREFIX)))
print("Derived bytes from prefix (hex):", derived.hex())

# assume repeating 4-byte key
KEY_LEN = 4
key = bytes(derived[:KEY_LEN])
print("Using repeating 4-byte key (hex):", key.hex())

# decrypt full cipher
plain = bytes(cipher[i] ^ key[i % KEY_LEN] for i in range(len(cipher)))
try:
    plain_text = plain.decode("utf-8")
except UnicodeDecodeError:
    plain_text = plain.decode("utf-8", errors="replace")

print("\nDecrypted preview:")
print(shorten(plain_text, width=400, placeholder="..."))
```

### Valaheadvala

Nah this is not a super-saiyan challenge, it's Krillin level.

Instruction: Get file from the server then reverse it. The flag is not on the server - no need to pentest it.

Author: Bankde

flag: `STDIO2025_17{n3XtlNeXt1n3xTIn3x7I_27323619a46c}`

```python
# extract_flag.py
from pathlib import Path

data = Path("challenge").read_bytes()

# offsets found in the binary's .rodata
t1 = data[0x2020:0x2020+48]    # 48 bytes
t2 = data[0x2050:0x2050+16]    # 16 bytes

flag_bytes = bytes(((t1[i] - t2[i % 16]) & 0xff) for i in range(48))
# strip trailing non-printable if any
flag = flag_bytes.rstrip(b'\x00\r\n\xff').decode('utf-8', errors='replace')
print(flag)
```
