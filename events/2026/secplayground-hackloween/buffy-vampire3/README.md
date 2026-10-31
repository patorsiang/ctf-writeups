# Buffy Vampire#3

## Metadata

- Event: SECPlayground Hackloween CTF 2026
- Category: Pwnable
- Points: 50
- Difficulty: Hard
- Tags: VM, HARD
- Solves: 20 at time of solve
- Status: Solved
- Target: `34.142.205.12:9999` over TCP. Ports `4444` and `4445` were listed as allowed but were not used.
- Files: [`vaultd`](extracted/vaultd), [`libc.so.6`](extracted/libc.so.6), [`ld-linux-x86-64.so.2`](extracted/ld-linux-x86-64.so.2), [`solve.py`](solve.py), [`try_paths.py`](try_paths.py)

## Problem Summary

> The Vesper Watch keeps its oldest secrets in a sealed vault archive, and the warden reseals it at every nightfall with a seal that is written down nowhere — it lives only in the warden's head while the vault is open. Behind the vault is a single record the Watch guards above all others. The archive answers to `vault>` over TCP. It is deliberately locked down: it refuses to do most of what a program can do. You get the archive program and its exact libraries. Make the archive produce its guarded record — the flag, pwnable{...}, chosen per instance. - The record lives at a path that includes the nightly seal, a 16-hex value minted when the vault boots. It is in no file you were given. - Only one internal routine ever opens and emits that record; the menu will not call it for you. The flag changes on every re-deploy.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Vulnerability Class

The exploit combines four weaknesses and primitives:

1. **Format-string vulnerability (CWE-134):** `cmd_inspect` passes the user-controlled note directly to `printf` as its format string. Positional specifiers make an out-of-bounds stack read. `%13$p` reveals the stack canary, and `%15$p` reveals a return address used to calculate the PIE base. This solve uses the bug only to read; it does not use `%n`.
2. **Intentional arbitrary-memory read:** `READAT` accepts a hex address and dumps 48 bytes from it. After calculating the PIE base, the exploit uses this menu primitive to read `g_token`, which holds the boot-time seal. The seal was not written to a file the attacker could read directly. This shows that an in-memory-only secret is only as safe as the program's available read primitives.
3. **Stack-based buffer overflow:** `cmd_archive` accumulates looping `read()` calls into an 80-byte stack buffer without checking the buffer's size. The 96-byte payload overwrites the canary, saved RBP, and return address.
4. **Return-address hijack to a linked function:** the payload restores the canary and returns to `emit_record`, a function present in the binary but absent from normal command dispatch. This is a ret2win, or ret2known-function, chain. It needs no ROP chain or libc leak because the target function is in the binary's own PIE image.

This binary has **Full RELRO**, unlike the **Partial RELRO** siblings. The read-only GOT would have foreclosed a GOT-overwrite approach using `%n`, even though this solve never attempted one. The binary also installs a seccomp filter through `install_sandbox`, which fits the prompt's note that the archive refuses many program operations. The designed approach reuses the binary's existing file-reading routine instead of relying on shellcode or a shell-oriented ROP chain.

## Binary Analysis

The download was `buffy_vampire3.zip`, with password `secplayground`. It contained `vaultd`, `libc.so.6`, and `ld-linux-x86-64.so.2`; the prompt supplied the exact runtime libraries. The binary is a dynamically linked, not-stripped x86-64 PIE ELF. It links against `libseccomp.so.2` and calls `install_sandbox` during startup.

Because the host machine is macOS/arm64 and the binary is amd64 Linux, `checksec` was run in the local `ctf-box` Docker image. It reported:

```text
Full RELRO
Stack Canary found
NX enabled
PIE enabled
SHSTK enabled
IBT enabled
Not stripped
```

All addresses below are static offsets within the PIE image. Add the process's randomized load base to get runtime addresses.

The menu commands are `MANIFEST`, `INSPECT <note>`, `READAT <hexaddr>`, `STASH`, `ARCHIVE`, `RESEAL`, `VERIFY`, `PURGE`, `HELP`, and `QUIT`. At startup, `main` reads up to 31 bytes from the first line of `/etc/vesper/vault.conf` into the global `g_token`, truncating at the first newline. This is the 16-hex-character nightly seal. The challenge files do not include the config file.

### `cmd_inspect`: format-string stack read

`cmd_inspect` starts at offset `0x15dc`. It copies up to `0x1f` bytes into a 32-byte stack buffer with `strncpy`, then passes that buffer directly to `printf` as the format string. Since the copy is not guaranteed to add a null terminator for a full-length input, and the call supplies no matching variadic arguments, positional probes can read stack values.

Local probes against the patched binary confirmed:

| Probe | Value |
| --- | --- |
| `INSPECT %13$p` | Stack canary; random per process, with a low byte of `0x00` |
| `INSPECT %15$p` | Return address into `main`, equal to PIE base + `0x1e64` |

The return address is the instruction after the call to `cmd_inspect` at `main` offset `0x1e5f`. Subtracting `0x1e64` from the leaked value recovers the PIE base. These are the same positional indices that worked for the matching format-string bug in Buffy Vampire#2.

### `cmd_readat`: arbitrary-memory read

`cmd_readat` starts at offset `0x1680`. It parses the supplied address with `strtoul` and dumps 48 bytes from that address, without validating whether the address is safe to read. The global `g_token` is at PIE offset `0x5040`, so `READAT` can disclose the seal after the format-string leak provides the PIE base. The returned bytes contain the seal as plain ASCII text.

### `cmd_stash`: stage the record path

`cmd_stash` starts at offset `0x17cc`. It clears the 256-byte `g_scratch` buffer at PIE offset `0x5060`, then reads at most 255 bytes into it and strips a trailing newline. This is bounded. The buffer is also the path that `emit_record` opens, so `STASH` gives the attacker control over that path once the seal is known.

### `cmd_archive`: stack overflow

`cmd_archive` starts at offset `0x1883`. Its stack frame reserves `0x60` bytes. The input buffer begins at `rbp-0x50`, and the canary sits at `rbp-0x8`: 72 bytes from the buffer start. Saved RBP is at offset 80 and the return address at offset 88.

After printing `send the archive frame: `, the handler repeatedly calls `read()` and accumulates input until it has collected `0x100` bytes or a read returns zero or an error. The loop does not check the real 80-byte buffer size. A 96-byte payload reaches the return address, but it is shorter than the loop's 256-byte target. The client must call `sock.shutdown(socket.SHUT_WR)` after sending it; the next `read()` sees EOF and lets the function return.

### `emit_record`: flag-printing function

`emit_record` is at PIE offset `0x14fa` and takes no arguments. It checks that `g_scratch` is non-empty, opens the staged path read-only, reads up to 256 bytes, writes them to standard output, closes the file, and exits. An empty path or failed `open()` produces an error and exits with status 1. Normal command dispatch never calls this function, matching the prompt's hint.

### `main`: config and command dispatch

`main` starts at offset `0x1cae`. Its startup code reads the seal into `g_token`, then runs the menu dispatch loop. The `call cmd_inspect` is at offset `0x1e5f`; its return address is `0x1e64`, which is the offset used to calculate the PIE base.

Buffy Vampire#3 is the third and hardest challenge in this series. Buffy Vampire#1 had no PIE and a static known path; #2 added PIE and needed an address leak but kept a static known path. #3 needs the PIE leak, a second read primitive to recover the runtime seal, and empirical discovery of the filename inside the sealed directory.

## Solution Walkthrough

### 1. Validate the binary locally

The binary was patched with `patchelf` to use the bundled loader and libc, then run in the local `ctf-box` Docker image under QEMU on the arm64 Mac. This confirmed the `%13$p` and `%15$p` positions and allowed the `READAT`, `STASH`, and `ARCHIVE` mechanics to be checked before connecting to the live target.

The local `install_sandbox()` call crashed under QEMU user-mode emulation. For local validation only, the five-byte `call install_sandbox` instruction at file offset `0x1d8f` was replaced with five NOPs. This was a QEMU emulation limitation, not a binary defect. The remote sandbox was left untouched. The exploit uses the existing `open`, `read`, `write`, and `close` behavior and did not need a seccomp bypass. The exact seccomp rule set was not enumerated.

### 2. Leak the canary and PIE base

On one connection, send `INSPECT %13$p` and `INSPECT %15$p`. The first value is the canary. The second is the return address into `main`; subtract `0x1e64` to get the PIE base. The solve script performs these calculations:

```python
    canary = leak_value(s, CANARY_POS)
    s.recv_until(b"vault> ")
    retaddr = leak_value(s, RETADDR_POS)
    s.recv_until(b"vault> ")

    pie_base = retaddr - RET_INTO_MAIN_OFFSET
```

### 3. Read the seal from memory

Calculate `g_token` as `PIE_base + 0x5040`, then send `READAT <hexaddr>`. The exploit trims the bytes at the first null and decodes the ASCII seal:

```python
    raw = readat(s, g_token_addr)
    seal = raw.split(b"\x00", 1)[0].decode(errors="replace")
```

The token varies by deployment. One local observation was `7948e586931772b7`; the solve script reads the current value instead of assuming it.

### 4. Find the filename inside the sealed directory

The `MANIFEST` flavor text showed the generic path template `Sealed vault: /var/vault/<sealed>`, but not the record's exact filename. The first attempt staged `/var/vault/<seal>` itself. The service printed its normal `archive frame committed` text, confirming that the return-address hijack reached `emit_record`, but returned neither a flag nor `record unavailable`.

That result suggested that `open()` had succeeded on the directory path, while the subsequent read produced no useful data. On Linux, opening a directory with `O_RDONLY` can succeed, but reading its directory descriptor does not return the record contents; `emit_record` does not report that read failure. This pointed to a file inside the sealed directory.

[`try_paths.py`](try_paths.py) repeated the full leak, seal-read, and return-hijack chain with fresh connections for candidate paths. Each connection needed a new canary and PIE base. The seal remained stable across those reconnects because the same config value was read at each boot. The helper tried names including `record`, `flag`, `record.dat`, `seal`, and `pwnable`. `/var/vault/<seal>/record.dat` returned the flag, matching the `record.dat` naming convention in Buffy Vampire#1.

### 5. Stage the path and redirect `ARCHIVE`

Send the confirmed path through `STASH`:

```python
    path = f"/var/vault/{seal}/record.dat"
```

Then send 72 filler bytes, the canary unchanged, eight saved-RBP filler bytes, and the runtime address of `emit_record` (`PIE_base + 0x14fa`):

```python
    payload = b"A" * 72
    payload += canary.to_bytes(8, "little")
    payload += b"C" * 8  # saved rbp, don't care
    payload += emit_record.to_bytes(8, "little")
```

The payload is 96 bytes. Half-close the socket after sending it so the read loop sees EOF and returns:

```python
    sock.shutdown(socket.SHUT_WR)
```

When `cmd_archive` returns, execution enters `emit_record`, which opens the staged file and sends its contents over the socket.

### 6. Observe and submit the flag

The live service returned:

```text
pwnable{EpQPNAxemr}
```

The platform's out-of-band validation did not register this solve, unlike Buffy Vampire#1 and #2. The flag was submitted manually through the challenge UI's answer box.

## Exploit / Script

[`solve.py`](solve.py) is the full solve script. It uses plain Python 3 and the standard-library `socket` module; it does not use pwntools. [`try_paths.py`](try_paths.py) documents the candidate-path search that found `record.dat`. The snippets above show the key leak, memory read, and payload without reproducing either full script.

## Flag

`pwnable{EpQPNAxemr}`

## Lessons Learned

- A format-string bug can disclose both a canary and a PIE return address. Those leaks defeat two separate mitigations.
- An intentional memory-read command can expose a secret that is never stored in an attacker-readable file. Review all read primitives when assessing secret storage.
- A loop that accumulates input still overflows a buffer when its total-input bound is unrelated to the buffer size. Half-closing a socket can end such a loop after a short payload.
- PIE requires a runtime address leak, but a linked function in the binary can still be called directly once the base is known. This avoids a libc leak and a ROP chain.
- Challenge flavor text can reveal the directory structure without revealing the filename. Treat silent behavior as evidence, then test candidate paths with a repeatable helper.
- Validate local exploit mechanics with the supplied runtime, but account for emulator limits. The local seccomp patch did not change the live target or its filter.

## References

- [`vaultd`](extracted/vaultd)
- [`libc.so.6`](extracted/libc.so.6)
- [`ld-linux-x86-64.so.2`](extracted/ld-linux-x86-64.so.2)
- [`solve.py`](solve.py)
- [`try_paths.py`](try_paths.py)
