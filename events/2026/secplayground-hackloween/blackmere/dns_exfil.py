"""Rebuild the DNS-tunnelled exfil blob from the Blackmere pcap. Offline only.

Same DNS-tunnel toolkit as events/2026/secplayground-hackloween/grimhollow/dns_exfil.py
(cfg-<hosttag> TXT handshake disguised as a DKIM record, carrying a 16-byte key
fragment; then chunked custom-base32 A-record queries; a "fin" marker with the
expected chunk count and a CRC32). Parameters differ per incident:

- host tag is derived from this host's MachineGuid (triage/registry), not a
  hardcoded value.
- the wire format here puts the chunk index in its own label instead of
  encoding it into the data label's first three characters.
"""
import base64
import binascii
import hashlib
import hmac
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
PCAP = HERE / "extracted/BMH-IR-2026-1013/capture/BMH-SHOWCTL-07_20261013.pcap"
AL = "lb3he5tc6z2qodyfxgavkjrmnspu4i7w"  # same custom base32 alphabet as grimhollow
MACHINE_GUID = "bed3068c-ea38-419c-b94e-ab6d20d90816"  # from triage/registry/HKLM_..._Cryptography.reg


def tshark(*args):
    return subprocess.run(["tshark", "-r", str(PCAP), *args], capture_output=True, text=True, check=True).stdout


def host_tag(guid: str) -> str:
    return hashlib.md5(guid.encode()).hexdigest()[:8]


def txt_records() -> list[str]:
    out = tshark("-Y", "dns.flags.response==1 && dns.qry.type==16", "-T", "fields", "-e", "dns.qry.name", "-e", "dns.txt")
    return [l for l in out.splitlines() if l]


def derive_key(ht: str, records: list[str]) -> bytes:
    for line in records:
        name, _, txt = line.partition("\t")
        if not name.startswith("cfg-" + ht):
            continue
        for sv in txt.replace(",", "").split(";"):
            kv = sv.split("=")
            if len(kv) > 1 and kv[0].strip() == "p":
                # unlike grimhollow, this incident's key is the raw TXT bytes,
                # not XORed with the host-tag mask (verified against the sid
                # that actually appears in the A-record exfil labels)
                return base64.b64decode("=".join(kv[1:]))[:16]
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
    chunks, final = {}, None
    for q in queries():
        lab = q.split(".")
        if sid not in lab:
            continue
        if len(lab) >= 3 and re.fullmatch(r"[0-9a-f]{4}", lab[0]) and lab[2] == "fin":
            final = (int(lab[0], 16), int(lab[1], 16))
            continue
        # <data>.<chunk-id hex4>.<session-id>.t.<domain>
        data, chunk_id = lab[0], lab[1]
        chunks[int(chunk_id, 16)] = data  # retries resend the same index
    n = len(chunks)
    en = "".join(chunks[i] for i in sorted(chunks))
    bits = "".join(f"{AL.index(c):05b}" for c in en)
    blob = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - len(bits) % 8, 8))
    n_expected, crc_expected = final
    crc = binascii.crc32(blob) & 0xFFFFFFFF
    kx = hashlib.sha256(k + guid.encode()).digest()
    iv, ct, mac = blob[:16], blob[16:-16], blob[-16:]
    mac_ok = hmac.new(kx, iv + ct, hashlib.sha256).digest()[:16] == mac
    plain = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-K", kx.hex(), "-iv", iv.hex()],
                            input=ct, capture_output=True).stdout
    return {"n": n, "n_expected": n_expected, "crc": crc, "crc_expected": crc_expected, "mac_ok": mac_ok, "plain": plain}


if __name__ == "__main__":
    r = recover(MACHINE_GUID)
    print({k: v for k, v in r.items() if k != "plain"})
    out = HERE / "artifacts"
    out.mkdir(exist_ok=True)
    (out / "exfil.bin").write_bytes(r["plain"])
