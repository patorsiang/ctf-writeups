"""Second theory: 'turn' means a byte-level transform of the 16-byte nonce
(matching Scenario.decode's XOR-by-0x5A house style), not a hash.
"""
import json
import urllib.request

HOST = "http://34.158.35.47"
SEED_KEY = "hearth-porch-6d13"


def req(method, path, headers=None, body=None, cookie=None):
    url = HOST + path
    data = body.encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        r.add_header(k, v)
    if cookie:
        r.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            return resp.status, resp.read().decode(), resp.headers.get("Set-Cookie")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), e.headers.get("Set-Cookie")


status, body, set_cookie = req("GET", "/api/v1/hearth/open", {"X-Hearth-Key": SEED_KEY})
nonce_hex = json.loads(body)["nonce"]
cookie = set_cookie.split(";")[0]
print("nonce:", nonce_hex)

nb = bytes.fromhex(nonce_hex)
candidates = {
    "xor_mask90": bytes(b ^ 0x5A for b in nb).hex(),
    "rotate_half": nonce_hex[16:] + nonce_hex[:16],
    "reversed_bytes": nb[::-1].hex(),
    "reversed_hexstr": nonce_hex[::-1],
    "xor_seed_cycled": bytes(b ^ SEED_KEY.encode()[i % len(SEED_KEY)] for i, b in enumerate(nb)).hex(),
    "upper": nonce_hex.upper(),
    "xor_mask90_then_rev": bytes(b ^ 0x5A for b in nb)[::-1].hex(),
}

for name, val in candidates.items():
    status, body, _ = req(
        "POST", "/api/v1/hearth/turn",
        {"X-Hearth-Key": SEED_KEY, "Content-Type": "application/json"},
        json.dumps({"turn": val, "nonce": nonce_hex}),
        cookie,
    )
    tag = "OK" if status == 200 else str(status)
    print(f"{name:22} {val:40} {tag:5} {body[:150]}")
    if status == 200:
        print("*** SUCCESS ***", name, val)
        break
