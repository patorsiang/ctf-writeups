"""Reassemble the DNS-name exfil: <hexbyte>.<idx>.data.exfiltrate.net queries from 192.168.1.42."""
import subprocess, re, sys, pathlib

PCAP = pathlib.Path("files/medium01-pcap-puzzle/capture.pcap")

def queries(src="192.168.1.42"):
    out = subprocess.run(["tshark", "-r", str(PCAP), "-Y",
        f"ip.src=={src} && dns.flags.response==0 && dns.qry.name contains \"exfiltrate.net\"",
        "-T", "fields", "-e", "frame.number", "-e", "frame.time_relative", "-e", "dns.qry.name"],
        capture_output=True, text=True, check=True).stdout.splitlines()
    for l in out:
        fn, t, name = l.split("\t")
        m = re.fullmatch(r"([0-9a-f]{2})\.(\d{4})\.data\.exfiltrate\.net", name)
        assert m, name
        yield int(fn), float(t), int(m.group(2)), int(m.group(1), 16)

def assemble(rows):
    by_idx = {}
    for fn, t, idx, b in rows:
        by_idx.setdefault(idx, []).append((fn, t, b))
    return by_idx

if __name__ == "__main__":
    by_idx = assemble(queries())
    print("indexes:", min(by_idx), "..", max(by_idx), "count", len(by_idx))
    print("dupes:", {i: v for i, v in by_idx.items() if len(v) > 1})
    missing = [i for i in range(min(by_idx), max(by_idx) + 1) if i not in by_idx]
    print("missing:", missing)
    data = bytes(by_idx[i][0][2] for i in sorted(by_idx))
    print(len(data), data.hex()); print(data)
