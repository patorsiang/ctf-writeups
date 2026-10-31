"""Reassemble client->server TCP payloads for port 8443 streams from 192.168.1.42.

Uses tshark's own reassembly (follow,tcp,raw) so segment reordering/retransmits
are handled by Wireshark, not by me. Output: one .bin per stream in streams/.
"""
import subprocess, pathlib, sys, collections

PCAP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "files/medium01-pcap-puzzle/capture.pcap")
OUT = pathlib.Path("streams"); OUT.mkdir(exist_ok=True)

def tshark(*a):
    return subprocess.run(["tshark", "-r", str(PCAP), *a], capture_output=True, text=True, check=True).stdout

rows = tshark("-Y", "ip.src==192.168.1.42 && tcp.dstport==8443 && tcp.len>0",
              "-T", "fields", "-e", "tcp.stream", "-e", "ip.dst").splitlines()
streams = collections.OrderedDict()
for r in rows:
    s, ip = r.split("\t"); streams[int(s)] = ip

def follow(n):
    out = tshark("-q", "-z", f"follow,tcp,raw,{n}")
    c2s = b""; s2c = b""
    for line in out.splitlines():
        if line.startswith("\t"):      # server -> client lines are tab-indented
            s2c += bytes.fromhex(line.strip())
        elif line and all(ch in "0123456789abcdef" for ch in line.strip()):
            c2s += bytes.fromhex(line.strip())
    return c2s, s2c

for n, ip in streams.items():
    c2s, s2c = follow(n)
    (OUT / f"s{n}_{ip}_c2s.bin").write_bytes(c2s)
    (OUT / f"s{n}_{ip}_s2c.bin").write_bytes(s2c)
    print(f"stream {n:3} {ip:15} c2s={len(c2s):5} s2c={len(s2c):5}")
