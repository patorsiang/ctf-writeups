#!/usr/bin/env python3
"""Candy Vault (mobile, hard) recon — reproducible checks, not throwaway curl.

Run: python3 recon.py
Each check prints PASS/FAIL against what we've actually observed from the
live server, so re-running after any server change tells us what moved.

State so far: APK (spgdrop-c05.apk) decompiled in jadx_out/. BuildConfig.CODE
= "c05", title "Courier". Scenario.java gives the X-Hearth-Key derivation
(XOR 90 over assets/hearth.properties: hearth.seed) and a turn(a,b) =
sha256(a+":"+b)[:16] helper — but turn() is never called anywhere in the
visible MainActivity code for c05, only Scenario.configure/path (the
"Check handset connection" health check).

Riddle: "the keeper's seal is on the keeper's slate, not on an ordinary
porch run" -> the /api/v1/hearth/open + /vault/board flow ("porch run") is
very likely a decoy. Confirmed facts below.
"""
import hashlib
import json
import sys
from urllib import request, error

HOST = "http://34.158.35.47"
KEY = "hearth-porch-6d13"  # decoded from hearth.properties via Scenario.decode


def req(method, path, headers=None, cookies=None, data=None):
    url = HOST + path
    h = dict(headers or {})
    if cookies:
        h["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    r = request.Request(url, method=method, headers=h, data=data)
    try:
        resp = request.urlopen(r, timeout=10)
        body = resp.read().decode("utf-8", "replace")
        return resp.status, dict(resp.getheaders()), body
    except error.HTTPError as e:
        return e.code, dict(e.headers.items()), e.read().decode("utf-8", "replace")


def get_cookie(headers):
    sc = headers.get("Set-Cookie", "")
    if sc.startswith("hollow_c05="):
        return sc.split(";")[0].split("=", 1)[1]
    return None


def open_session():
    code, headers, body = req("GET", "/api/v1/hearth/open", {"X-Hearth-Key": KEY})
    assert code == 200, f"expected 200 opening session, got {code}: {body}"
    cookie = get_cookie(headers)
    assert cookie, "no hollow_c05 cookie set"
    nonce = json.loads(body)["nonce"]
    return cookie, nonce


def check_xhearth_key_rejects_anything_but_base():
    """X-Hearth-Key only ever accepts the literal decoded seed — never a
    turn(nonce,key) value in any order/encoding we've tried."""
    cookie, nonce = open_session()
    candidates = {
        "nk_colon_str": hashlib.sha256(f"{nonce}:{KEY}".encode()).hexdigest()[:16],
        "kn_colon_str": hashlib.sha256(f"{KEY}:{nonce}".encode()).hexdigest()[:16],
        "nk_nocolon": hashlib.sha256(f"{nonce}{KEY}".encode()).hexdigest()[:16],
        "kn_nocolon": hashlib.sha256(f"{KEY}{nonce}".encode()).hexdigest()[:16],
    }
    for name, val in candidates.items():
        code, _, body = req("GET", "/api/v1/hearth/open", {"X-Hearth-Key": val}, {"hollow_c05": cookie})
        assert code == 403 and "not accepted" in body, f"{name}: expected rejection, got {code} {body}"
    print("PASS: X-Hearth-Key rejects every turn(nonce,key) variant tried; only the base seed works")


def check_vault_board_always_403_regardless_of_auth():
    """/vault/board returns the same 403 'Dispatch session required' no
    matter what cookie/bearer/header combination we send."""
    cookie, nonce = open_session()
    # plain cookie
    code, _, body = req("GET", "/vault/board", cookies={"hollow_c05": cookie})
    assert code == 403 and "Dispatch session required" in body
    # + driver bearer token (fresh login)
    code2, _, body2 = req(
        "POST",
        "/api/v1/driver/session",
        {"Content-Type": "application/json"},
        data=json.dumps({"email": "alice.morgan@hollowpost.test", "password": "NorthDepot!31"}).encode(),
    )
    assert code2 == 200, body2
    token = json.loads(body2)["access_token"]
    code3, _, body3 = req("GET", "/vault/board", {"Authorization": f"Bearer {token}"}, {"hollow_c05": cookie})
    assert code3 == 403 and "Dispatch session required" in body3
    print("PASS: /vault/board stays 403 with hearth cookie, driver bearer token, or both together")


def check_no_vhost_routing():
    """Host-header vhost routing to a 'keeper'/'vault' backend does not exist
    — every Host guess returns the identical 3121-byte homepage."""
    sizes = set()
    for host_hdr in ["keeper.hollowpost.test", "vault.hollowpost.test", "dispatch.hollowpost.test", HOST.split("//")[1]]:
        code, _, body = req("GET", "/", {"Host": host_hdr})
        sizes.add(len(body.encode()))
    assert len(sizes) == 1, f"vhosts differ in size: {sizes} — worth re-investigating!"
    print("PASS: no Host-header vhost routing found (all identical homepage)")


def check_flask_secret_not_in_common_wordlist():
    """hollow_c05 is a standard itsdangerous/Flask session cookie
    ({'porch_nonce': ...}); flask-unsign against the 56k-word default
    wordlist found nothing. Not re-run here (slow); recorded as fact."""
    print("INFO (not re-run, slow): flask-unsign default wordlist (55982 words) found no secret for hollow_c05")


if __name__ == "__main__":
    for fn in [
        check_xhearth_key_rejects_anything_but_base,
        check_vault_board_always_403_regardless_of_auth,
        check_no_vhost_routing,
        check_flask_secret_not_in_common_wordlist,
    ]:
        fn()

    print(
        "\nOPEN QUESTION: how is a 'dispatch session' actually established for "
        "/vault/board? Every mechanism visible in the c05 APK (hearth key check, "
        "driver bearer login) has been tried and rejected. Backup extraction is "
        "a dead end too — res/xml/backup_rules.xml explicitly excludes sharedpref "
        "from full-backup-content, so there's nothing to pull off-device even "
        "with adb backup. Riddle text says the flag isn't on the 'porch run' "
        "(this whole hearth/vault flow) at all, so the real endpoint is probably "
        "something not linked from the app or homepage nav that we haven't found."
    )
