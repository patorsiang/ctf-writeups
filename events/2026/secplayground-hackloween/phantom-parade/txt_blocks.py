"""Collect inbound DNS TXT answers (16-byte base64 blocks) and try AES with the cfg value as key."""
import subprocess, base64, re, pathlib
from Crypto.Cipher import AES   # pycryptodome; run with ../../../../.venv/bin/python

P = pathlib.Path("files/medium01-pcap-puzzle/capture.pcap")

def txt_answers():
    out = subprocess.run(["tshark", "-r", str(P), "-Y", "ip.dst==192.168.1.42 && dns.txt",
        "-T", "fields", "-e", "frame.time_relative", "-e", "dns.qry.name", "-e", "dns.txt"],
        capture_output=True, text=True, check=True).stdout.splitlines()
    res = {}
    for l in out:
        t, n, v = l.split("\t"); res[n] = (float(t), base64.b64decode(v))
    return res

def printable(b): return sum(32 <= c < 127 for c in b) / max(len(b), 1)

if __name__ == "__main__":
    ans = txt_answers()
    key = ans["cfg.sync-telemetry-cdn.net"][1]
    nodes = [ans[f"node-{i:02d}.lanterns.hollowmere.test"][1] for i in range(12)]
    ct = b"".join(nodes)
    print("key", key.hex(), "ct", len(ct))
    print("raw printable", printable(ct))
    for name, pt in [("ecb", AES.new(key, AES.MODE_ECB).decrypt(ct)),
                     ("cbc-iv0", AES.new(key, AES.MODE_CBC, bytes(16)).decrypt(ct)),
                     ("ctr-0", AES.new(key, AES.MODE_CTR, nonce=bytes(8)).decrypt(ct))]:
        print(name, f"{printable(pt):.2f}", pt[:64])
