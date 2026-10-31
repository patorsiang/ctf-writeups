"""Reproduce MainActivity.permit(body, secret) client-side, with our own chosen
permit_role, and present it directly to /yard/board — bypassing the server's
/api/yard/v2/release endpoint (which only ever echoes our own account role).

permit(str, secret) in the app:
  encoded = base64url_nopad(str.bytes)
  sig = base64url_nopad(HMAC-SHA256(key=secret, msg=encoded.bytes))
  return encoded + "." + sig
"""
import base64
import hashlib
import hmac
import urllib.request

HOST = "http://34.126.107.145"
SECRET = "d7c2ae935c2087da6338230c04af3460"  # today's (10-31) device_secret


def b64url_nopad(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def permit(body: str, secret: str) -> str:
    encoded = b64url_nopad(body.encode())
    sig = b64url_nopad(hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).digest())
    return f"{encoded}.{sig}"


def get(path: str, headers: dict) -> tuple:
    r = urllib.request.Request(HOST + path, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


TOKEN = "yd-c7d05231e69e"

for key_name, key in [("device_secret", SECRET), ("api_token", TOKEN)]:
    for role in ["driver", "yardmaster"]:
        body = '{"stop":"A-101","permit_role":"%s"}' % role
        perm = permit(body, key)
        status, text = get("/yard/board", {"X-Yard-Local": perm})
        bad = "has not signed" in text
        print(f"key={key_name:14} role={role:11} status={status} signed={not bad}")
        if not bad:
            for line in text.splitlines():
                if "seal" in line.lower() or "mobile{" in line:
                    print("  SEAL LINE:", line.strip())
