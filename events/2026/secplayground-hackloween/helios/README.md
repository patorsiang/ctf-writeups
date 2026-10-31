# Helios

## Metadata

- Event: SECPlayground Hackloween CTF 2026
- Category: Web Application Security
- Points: 30
- Difficulty: Medium
- Tags: VM, MEDIUM
- Solves: 24 at time of solve; most-solved challenge in the Web category
- Status: Solved
- Target: `35.198.204.5:80` over plain HTTP (Helios Ops Portal)
- Flag format: `web{...}`
- Files: [`solve.py`](solve.py), [`test_solve.py`](test_solve.py), [`artifacts/realm-helios.json`](artifacts/realm-helios.json), [`artifacts/realm-helios.pretty.json`](artifacts/realm-helios.pretty.json)

## Problem Summary

> Read the Helios control-plane recovery secret out of the credential vault at `/vault` on the Helios Ops Portal. You have no credentials, no mailbox, and the vault is gated on a realm role that only the platform administrators hold.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Vulnerability Class

The solve chained an unrestricted path traversal in the public runbook renderer with plaintext credentials in the Keycloak realm import. The import identified the only `platform-admin` user. Those credentials granted access through the portal's login form, and the resulting Flask session could read `/vault`.

## Reconnaissance

`GET /` showed a Flask portal in front of Keycloak. The page named realm `helios` and client `helios-portal`, and linked to:

- `/vault`, restricted to holders of the `platform-admin` realm role.
- `/realms/helios/account/`, the Keycloak account console.
- `/realms/helios/login-actions/reset-credentials?client_id=helios-portal`, for password reset.
- `/ops/runbooks`, a public runbook index.

`GET /ops/runbooks` listed five documents: `access-review.md`, `backup.md`, `idp.md`, `index.md`, and `oncall.md`. Its footer said, “The renderer prints Markdown and JSON. Anything else is refused.” The renderer allowed file types by extension, but did not confine reads to the runbook directory.

Reading `idp.md` through the renderer exposed the realm import path and its purpose:

```text
# Helios SSO — Keycloak

* Product: Keycloak 26.7.1, single node, dev-file (H2) store.
* Bound to 127.0.0.1:8081; the edge publishes it under /realms/, /resources/ and /admin/.
* Realm: `helios`. It is imported at boot from:

      /opt/keycloak/data/import/realm-helios.json

  That file is the source of truth for clients, roles, users and role mappings.
  To review who holds a realm role, read the export — do not query the admin API,
  which is rate-limited on this host.
* Self-service password recovery is enabled realm-wide. Recovery links are mailed
  to the address on file and expire after 5 minutes.
* Mail leaves through the local sink on 127.0.0.1:1025; nothing reaches the public
  internet from this host.
```

`access-review.md` said the portal performs no authorization of its own and trusts the role asserted by Helios SSO. It also named the realm configuration as the authoritative source for `platform-admin` membership.

## Path Traversal and Realm Export

The renderer accepted a plain traversal in the `doc` parameter:

```http
GET /ops/runbook?doc=../../../../opt/keycloak/data/import/realm-helios.json
```

The response was `200 OK` with `Content-Type: text/plain; charset=utf-8` and contained the complete realm import. A URL-encoded traversal behaved the same way. A double-encoded traversal returned `404 no such runbook: ...`, showing that the query string was decoded once before the unsanitized filesystem read.

The export contained user passwords in plaintext, along with realm-role assignments. Its realm roles included `platform-admin` and `staff`. The only provided user record assigned `platform-admin` was:

```json
{
  "username": "k.thepsuwan",
  "email": "k.thepsuwan@helios.internal",
  "credentials": [
    {
      "type": "password",
      "value": "Wq5-Helios-Platform-2026-nH",
      "temporary": false
    }
  ],
  "realmRoles": ["default-roles-helios", "platform-admin", "staff"]
}
```

The complete raw capture is in [`artifacts/realm-helios.json`](artifacts/realm-helios.json); [`artifacts/realm-helios.pretty.json`](artifacts/realm-helios.pretty.json) formats the same export for reading.

The public `helios-portal` client had `directAccessGrantsEnabled: true`. A password-grant request to `/realms/helios/protocol/openid-connect/token` accepted the recovered credential. The returned JWT included `platform-admin` in `realm_access.roles`, confirming the credential against Keycloak independently of the portal form.

## Solution Walkthrough

### 1. Read the public runbooks

The team moved to Helios after ItsCloud, a 0-solve challenge, proved to be a dead end. Helios had 24 solves and was the most-solved challenge in the Web category. The public runbook index exposed `idp.md`, which documented the exact boot-time realm import path.

### 2. Read the realm import with traversal

Request the JSON export through `/ops/runbook` using the path shown in `idp.md`. The endpoint returned the complete file even though it was outside the runbook directory.

### 3. Select the realm administrator

Parse the export and find the enabled user whose `realmRoles` include `platform-admin`. The export identified `k.thepsuwan` and provided a non-temporary plaintext password. The direct password-grant check confirmed that Keycloak accepted it and returned a token with the expected role.

### 4. Log in through the portal

The portal's `/login` page was a plain HTML form. A bearer token sent directly to `/vault` received a `302` redirect to `/login` with the flash message “Sign in with your Helios account to continue.” The portal required its own session cookie.

Submitting the recovered credentials to the portal form returned `302 FOUND`, redirected to `/vault`, and set a Flask `session` cookie:

```http
POST /login
username=k.thepsuwan&password=Wq5-Helios-Platform-2026-nH
```

The Flask backend performed the Keycloak password-grant exchange server-side. This flow used the portal form and its session cookie, not a browser-redirect authorization-code flow.

### 5. Read and submit the secret

Request `/vault` with the new session cookie. It returned `200 OK`, identified Kanya Thepsuwan (`k.thepsuwan`), showed the `platform-admin` role, and displayed:

```text
Helios control-plane recovery secret
web{mWeZXmT5a3}
```

The flag was submitted through the in-game ANSWER box and confirmed correct. The score changed from 140 to 170, and the live feed recorded “Ostrich00 Captured Helios +30”. After capture, the Helios VM timed out while other hosts remained reachable from the same network. This is consistent with VM teardown or recycling; the challenge was solved and confirmed.

## Exploit / Script

[`solve.py`](solve.py) automates the full chain: fetch the realm export through traversal, select the enabled `platform-admin` user, submit credentials through `/login`, retain the Flask session cookie, read `/vault`, and extract the flag with a regular expression. It uses only Python's standard-library `urllib` and `http.cookiejar` modules. The script ran against the live target before the VM went down and printed the flag end-to-end.

[`test_solve.py`](test_solve.py) contains three offline tests for `find_platform_admin`, using the realm export captured during the live solve and two synthetic negative cases: a staff-only user and a disabled administrator. All three tests pass with:

```sh
uv run --with pytest pytest test_solve.py
```

These tests cover export parsing only. The traversal, login, and vault read were exercised live; the HTTP responses above record that network leg. The tests do not rerun it against the unavailable VM.

## Flag

`web{mWeZXmT5a3}`

## Lessons Learned

- A file used only at boot still belongs to the attack surface if an endpoint can be tricked into reading arbitrary paths.
- An extension allow-list does not prevent path traversal. File-reading endpoints should confine resolved paths to the intended directory.
- Keycloak realm exports are administrative bootstrap artifacts, not secret-safe configuration files. This export contained plaintext passwords and role assignments.
- Trusting an identity provider's role claim can work when credentials remain protected. Here, the credentials were exposed, so the portal's role-based gate could be satisfied.
- A public OIDC client with the direct-grant flow enabled made it possible to validate the recovered credential at Keycloak separately from the portal's session-cookie requirement.

## References

- [`solve.py`](solve.py)
- [`test_solve.py`](test_solve.py)
- [`artifacts/realm-helios.json`](artifacts/realm-helios.json)
- [`artifacts/realm-helios.pretty.json`](artifacts/realm-helios.pretty.json)
