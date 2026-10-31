"""Tests for the DNS exfil recovery. Verify by RECONSTRUCTION: re-encode the value, compare to the capture."""
import hashlib, pathlib, subprocess
import dns_exfil

PCAP = pathlib.Path("files/medium01-pcap-puzzle/capture.pcap")
VALUE = b"svc-backup:Restore#Wgx7Q2r!vpn-2024"

def test_input_pinned():
    assert PCAP.stat().st_size == 550749
    assert hashlib.sha256(PCAP.read_bytes()).hexdigest() == \
        "6c455a3412e829b6bde418e5ac2dcf56b95099b5fc6b11872e7acb87b0ad53ac"

def observed():
    return dns_exfil.assemble(dns_exfil.queries())

def test_complete_channel_no_gaps_no_dupes():
    by_idx = observed()
    assert sorted(by_idx) == list(range(1, 36))
    assert all(len(v) == 1 for v in by_idx.values())

def test_decoded_value():
    by_idx = observed()
    assert bytes(by_idx[i][0][2] for i in sorted(by_idx)) == VALUE

def test_reconstruction_matches_capture_exactly():
    expected = {f"{b:02x}.{i:04d}.data.exfiltrate.net" for i, b in enumerate(VALUE, 1)}
    out = subprocess.run(["tshark", "-r", str(PCAP), "-Y",
        'ip.src==192.168.1.42 && dns.flags.response==0 && dns.qry.name contains "exfiltrate.net"',
        "-T", "fields", "-e", "dns.qry.name"], capture_output=True, text=True, check=True).stdout.split()
    assert set(out) == expected and len(out) == len(expected)

def test_only_suspect_host_queries_exfil_domain():
    out = subprocess.run(["tshark", "-r", str(PCAP), "-Y",
        'dns.flags.response==0 && dns.qry.name contains "exfiltrate.net"',
        "-T", "fields", "-e", "ip.src"], capture_output=True, text=True, check=True).stdout.split()
    assert set(out) == {"192.168.1.42"}

def test_every_query_was_acknowledged_noerror():
    out = subprocess.run(["tshark", "-r", str(PCAP), "-Y",
        'dns.flags.response==1 && dns.qry.name contains "exfiltrate.net"',
        "-T", "fields", "-e", "dns.flags.rcode"], capture_output=True, text=True, check=True).stdout.split()
    assert len(out) == 35 and set(out) == {"0"}
