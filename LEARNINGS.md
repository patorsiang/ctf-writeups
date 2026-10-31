# Learnings Log

Append-only log of things worth fixing in how this repo's CTF work gets done —
correctness mistakes, workflow/process patterns, or anything surfaced in an
"improve me" recap. Never edit an old entry; add a new one instead, even if it
corrects a previous one.

Format: `### YYYY-MM-DD — event / topic — one-line title`, then what happened,
**Why it matters**, **Do differently**.

## Entries

### 2026-10-31 — SECPlayground Hackloween — scratch-probing over saved scripts
`candy-vault` accumulated 9 probe/turn_* scripts (`driver_flow.sh`,
`probe_keeper.sh`, `turn_xor.py`, etc.) chasing a brute force that never
converged, with no README recording what was ruled out.

**Why it matters:** same pattern already caught once during Too Loud To Yap
(2026-07-31) — analysis that isn't saved and tested is unreproducible, and
probing without recording failures burns time re-deriving the same dead ends.

**Do differently:** after ~3 probe attempts without a hit, stop and write down
what's ruled out before trying variant 4.

### 2026-10-31 — SECPlayground Hackloween — README lag mid-competition
7 of 12 challenge folders had no README by mid-match (blackmere, candy-vault,
disaster-elephant, grimhollow, grimhollow-studios, phantom-parade,
poisoned-package, yard-release); only buffy-vampire1-3, helios, night-claim,
and legacy-intake were documented.

**Why it matters:** reconstruction value drops fast once the match ends and
the "why I tried X" context is gone from memory.

**Do differently:** write the README the moment a challenge is solved or
abandoned, not after the match ends.

### 2026-10-31 — SECPlayground Hackloween — near-miss committing fake secrets
A pre-push cleanup caught a GitHub-PAT-shaped string, npm/SSH credential
files, and an AWS-key-shaped string in challenge evidence/solve scripts
(`grimhollow/artifacts/exfil*`, `phantom-parade/blob_brute.py`) — fake CTF
data, but GitHub's push protection treats them as real and will block or flag
a push.

**Why it matters:** a blocked push mid-competition costs time, and secret
scanning doesn't know "this is a fictional incident-response challenge."

**Do differently:** before any commit in a live-CTF event folder, grep new
files for PAT/AWS-key/credential-file shapes; gitignore anything regenerable
from an already-ignored zip/apk, and expect to use GitHub's "allow this
secret" unblock link for load-bearing fake values that must stay (e.g. a key
a solve script brute-forces against).
