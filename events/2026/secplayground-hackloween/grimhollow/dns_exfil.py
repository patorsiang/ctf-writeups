"""Rebuild the DNS-tunnelled stage-2 exfil (artifacts/stage2.ps1.txt) from the pcap. Offline only."""
import base64
import binascii
import hashlib
import hmac
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PCAP = HERE / "files/GHS-IR-2026-1018/capture/GHS-EDIT-01_20261018.pcap"
AL = "lb3he5tc6z2qodyfxgavkjrmnspu4i7w"  # custom base32 alphabet from $al


def tshark(*args):
    return subprocess.run(["tshark", "-r", str(PCAP), *args], capture_output=True, text=True, check=True).stdout


def host_tag(guid: str) -> str:
    return hashlib.md5(guid.encode()).hexdigest()[:8]


def txt_records() -> list[str]:
    out = tshark("-Y", "dns.flags.response==1 && dns.qry.type==16", "-T", "fields", "-e", "dns.qry.name", "-e", "dns.txt")
    return [l for l in out.splitlines() if l]


def derive_key(ht: str, records: list[str]) -> bytes:
    hb = (ht + ht).encode()
    for line in records:
        name, _, txt = line.partition("\t")
        if not name.startswith("cfg-" + ht):
            continue
        for sv in txt.replace(",", "").split(";"):
            kv = sv.split("=")
            if len(kv) > 1 and kv[0].strip() == "p":
                pb = base64.b64decode("=".join(kv[1:]))[:16]
                return bytes(a ^ b for a, b in zip(pb, hb))
    raise LookupError("no p= TXT answer")


def session_id(k: bytes) -> str:
    return hashlib.sha256(k).hexdigest()[:8]


def queries() -> list[str]:
    out = tshark("-Y", "dns.flags.response==0 && dns.qry.type==1", "-T", "fields", "-e", "dns.qry.name")
    return out.split()


def recover(guid: str) -> dict:
    ht = host_tag(guid)
    k = derive_key(ht, txt_records())
    sid = session_id(k)
    m = int(sid[4:8], 16) & 0x7FFF
    chunks, final = {}, None
    for q in queries():
        lab = q.split(".")
        if sid not in lab:
            continue
        if re.fullmatch(r"[0-9a-f]{4}", lab[0]) and lab[2] == "fin":
            final = (int(lab[0], 16), int(lab[1], 16))
            continue
        tag, cx = lab[0][:3], lab[0][3:]
        v = (AL.index(tag[0]) << 10) | (AL.index(tag[1]) << 5) | AL.index(tag[2])
        chunks.setdefault(v ^ m, cx)  # retries resend the same index
    n = len(chunks)
    en = "".join(chunks[i] for i in sorted(chunks))
    bits = "".join(f"{AL.index(c):05b}" for c in en)
    bl = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - len(bits) % 8, 8))
    n_expected, crc_expected = final
    blob = bl  # trailing <8 pad bits drop out via the %8 trim above
    crc = binascii.crc32(blob) & 0xFFFFFFFF
    kx = hashlib.sha256(k + guid.encode()).digest()
    iv, ct, mac = blob[:16], blob[16:-16], blob[-16:]
    mac_ok = hmac.new(kx, iv + ct, hashlib.sha256).digest()[:16] == mac
    plain = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-K", kx.hex(), "-iv", iv.hex()],
                           input=ct, capture_output=True).stdout
    return {"n": n, "n_expected": n_expected, "crc": crc, "crc_expected": crc_expected, "mac_ok": mac_ok, "plain": plain}



if __name__ == "__main__":
    r = recover("60cb634d-1345-47f0-b256-293afe32b6e9")
    print({k: v for k, v in r.items() if k != "plain"})
    (HERE / "artifacts/exfil.zip").write_bytes(r["plain"])
