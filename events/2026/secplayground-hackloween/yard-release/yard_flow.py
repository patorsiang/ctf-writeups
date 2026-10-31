"""Reproduce Scenario.sign()/release() against the live Yard Release target.

sign(method, path, ts, secret) = hex(HMAC-SHA256(f"{method}\n{path}\n{ts}", secret))
"""
import hashlib
import hmac
import time
import urllib.request

HOST = "http://34.126.107.145"
TOKEN = "yd-c7d05231e69e"
SECRET = "d7c2ae935c2087da6338230c04af3460"
STOPS = "/api/yard/v2/stops"
RELEASE = "/api/yard/v2/release"


def sign(method, path, ts, secret):
    msg = f"{method}\n{path}\n{ts}".encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def call(method, path, body=None):
    ts = str(int(time.time()))
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "X-Yard-Ts": ts,
        "X-Yard-Sig": sign(method, path, ts, SECRET),
    }
    data = body.encode() if body else None
    if body:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(HOST + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


status, body = call("GET", STOPS)
print("GET stops:", status, body[:500])

status, body = call("POST", RELEASE, '{"stop":"A-101","permit_role":"driver"}')
print("POST release (driver):", status, body[:500])

status, body = call("POST", RELEASE, '{"stop":"A-101","permit_role":"yardmaster"}')
print("POST release (yardmaster):", status, body[:500])
