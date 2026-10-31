"""Systematic sweep of candidate 'turn' values against the live Candy Vault
/api/v1/hearth/turn endpoint, reusing one session/nonce (server allows repeat
attempts per nonce, confirmed by prior manual testing).

Run with: python3 turn_wide.py
"""
import hashlib
import hmac as hmaclib
import json
import urllib.request

HOST = "http://34.158.35.47"
SEED_KEY = "hearth-porch-6d13"
TOKEN = "cturnG_IkB0DFsKXIZPWlQvW-OUzlgIfDXDoSv9lBEA"


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


# 1. open a session
status, body, set_cookie = req("GET", "/api/v1/hearth/open", {"X-Hearth-Key": SEED_KEY})
print("open:", status, body)
nonce = json.loads(body)["nonce"]
cookie = set_cookie.split(";")[0]
print("nonce:", nonce, "cookie:", cookie)

candidates = {}
for key_name, key in [("seed", SEED_KEY), ("token", TOKEN)]:
    for order_name, a, b in [("n_k", nonce, key), ("k_n", key, nonce)]:
        digest = hashlib.sha256(f"{a}:{b}".encode()).hexdigest()
        candidates[f"sha256({order_name},{key_name})16"] = digest[:16]
        candidates[f"sha256({order_name},{key_name})64"] = digest
    h1 = hmaclib.new(key.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    h2 = hmaclib.new(nonce.encode(), key.encode(), hashlib.sha256).hexdigest()
    candidates[f"hmac(key={key_name},msg=nonce)16"] = h1[:16]
    candidates[f"hmac(key={key_name},msg=nonce)64"] = h1
    candidates[f"hmac(key=nonce,msg={key_name})16"] = h2[:16]
    candidates[f"hmac(key=nonce,msg={key_name})64"] = h2

for name, val in candidates.items():
    status, body, _ = req(
        "POST", "/api/v1/hearth/turn",
        {"X-Hearth-Key": SEED_KEY, "Content-Type": "application/json"},
        json.dumps({"turn": val, "nonce": nonce}),
        cookie,
    )
    tag = "OK" if status == 200 else str(status)
    print(f"{name:32} {tag:5} {body[:120]}")
    if status == 200:
        print("*** SUCCESS ***", name, val)
        break
