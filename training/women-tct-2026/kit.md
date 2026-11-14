# Competition Kit

Check it: `sh tools/check_kit.sh`. It only reports and never installs.
Get the missing list down to zero by **2026-11-21** (W1). Re-check on 12-11 and 12-25.

## Tools per category

| Category | Tool | Verify |
|---|---|---|
| web | curl | `curl --version` |
| web | Burp Suite Community | open the app, proxy on 127.0.0.1:8080 |
| web | ffuf | `ffuf -V` |
| forensics | file, strings | `file --version` |
| forensics | exiftool | `exiftool -ver` |
| forensics | binwalk | `binwalk --help` |
| forensics | foremost | `foremost -V` |
| forensics | volatility3 | `vol -h` |
| re-pwn | Ghidra | `ghidraRun` opens |
| re-pwn | gdb + pwndbg, checksec | inside the Linux container (below): `gdb -q -ex quit` |
| re-pwn | pwntools | `python -c "import pwn"` (kit venv) |
| network | Wireshark / tshark | `tshark -v` |
| mobile | jadx | `jadx --version` |
| mobile | apktool | `apktool --version` |
| programming | pwntools (nc scripting) | `python -c "import pwn"` |
| crypto | pycryptodome, sympy, gmpy2 | `python -c "import Crypto, sympy, gmpy2"` |
| crypto | SageMath (optional; it's large) | `sage -v` |
| misc | CyberChef (offline HTML) | open `~/ctf-kit/cyberchef/CyberChef.html` |
| misc | steghide, zsteg | `steghide --version`, `zsteg -h` |
| ai-iot | binwalk, strings | as above |

**Pwn on a Mac:** gdb doesn't run natively on Apple Silicon. Use a Linux x86-64
container instead, with gdb, pwndbg, checksec and pwntools inside it. Docker is
already installed. Build the image in W1, while there's internet.

## Offline

Assume the final may have no internet until the rules say otherwise.

- **Kit venv:** `~/.venvs/ctf` with pwntools, pycryptodome, sympy, gmpy2, requests. Pin
  the versions in `~/ctf-kit/requirements.txt`.
- **Wordlists:** `~/ctf-kit/wordlists/`: rockyou.txt, plus a SecLists subset
  (Discovery/Web-Content common lists, Passwords top lists).
- **Docs:** `~/ctf-kit/docs/`: CyberChef, saved copies of the repo's `notes/` triage
  playbooks, pwntools cheat sheet, Python `struct`/`bytes` reference.
- **Container:** the pwn image is built and tagged locally. `docker images` lists it
  with no network.

## Competition-day routine

1. **First 15 min:** scan the whole board, then rank by points per expected minute. Easy challenges in every category come first.
2. **Time-box each challenge:** easy 30 min, medium 60 min. Past the box, write what's ruled out and move on.
3. **README stub** the moment a challenge is solved or dropped (the Hackloween lesson).
4. **Qualifier (AI allowed):** you drive and Claude pairs. Agents only take grindy sub-tasks, and only on local files until the organizer confirms "AI allowed" covers them.
5. **Final (no AI):** use the offline docs and your notes, if the rules allow notes.
6. **Before a commit in an event folder:** grep the new files for credential-shaped
   strings first (see LEARNINGS.md, 2026-10-31, "near-miss committing fake secrets").
