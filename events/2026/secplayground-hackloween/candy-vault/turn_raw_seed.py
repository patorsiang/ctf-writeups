"""Last cheap theory: the RAW undecoded hearth.seed string (colons and all)
is the key material for 'turn', not the XOR-decoded 'hearth-porch-6d13'.
"""
import hashlib
import hmac as hmaclib
import json
import urllib.request

HOST = "http://34.158.35.47"
SEED_KEY = "hearth-porch-6d13"  # for X-Hearth-Key header (confirmed correct for /open)
RAW_SEED = "32:3f:3b:28:2e:32:77:2a:35:28:39:32:77:6c:3e:6b:69"


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
nonce = json.loads(body)["nonce"]
cookie = set_cookie.split(";")[0]
print("nonce:", nonce)

candidates = {}
for order_name, a, b in [("n_k", nonce, RAW_SEED), ("k_n", RAW_SEED, nonce)]:
    d = hashlib.sha256(f"{a}:{b}".encode()).hexdigest()
    candidates[f"sha256({order_name})16"] = d[:16]
    candidates[f"sha256({order_name})64"] = d
h1 = hmaclib.new(RAW_SEED.encode(), nonce.encode(), hashlib.sha256).hexdigest()
h2 = hmaclib.new(nonce.encode(), RAW_SEED.encode(), hashlib.sha256).hexdigest()
candidates["hmac(key=rawseed)16"] = h1[:16]
candidates["hmac(key=rawseed)64"] = h1
candidates["hmac(key=nonce,msg=rawseed)16"] = h2[:16]
candidates["hmac(key=nonce,msg=rawseed)64"] = h2

for name, val in candidates.items():
    status, body, _ = req(
        "POST", "/api/v1/hearth/turn",
        {"X-Hearth-Key": SEED_KEY, "Content-Type": "application/json"},
        json.dumps({"turn": val, "nonce": nonce}),
        cookie,
    )
    tag = "OK" if status == 200 else str(status)
    print(f"{name:28} {tag:5} {body[:120]}")
    if status == 200:
        print("*** SUCCESS ***", name, val)
        break
