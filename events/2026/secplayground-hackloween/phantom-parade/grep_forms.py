"""Search a file for a needle in raw / reversed / hex / base64 (3 alignments) / base32 forms."""
import base64, sys, pathlib
needle = sys.argv[1].encode(); data = pathlib.Path(sys.argv[2]).read_bytes()
forms = {"raw": needle, "rev": needle[::-1], "hex": needle.hex().encode(), "HEX": needle.hex().upper().encode()}
for i in range(3):
    forms[f"b64+{i}"] = base64.b64encode(b"\0" * i + needle)[ (i * 4 + 2) // 3 if i else 0 : -2 or None]
forms["b32"] = base64.b32encode(needle).rstrip(b"=")
for n, f in forms.items():
    k = data.find(f)
    print(f"{n:7} {'FOUND @%d' % k if k >= 0 else '-'}")
