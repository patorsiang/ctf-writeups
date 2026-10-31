# Buffy Vampire#1

## Metadata

- Event: SECPlayground Hackloween CTF 2026
- Category: Pwnable
- Points: 10
- Difficulty: Easy
- Tags: VM, EASY
- Solves: 26 at time of solve
- Status: Solved
- Target: `136.85.48.133:9999` over TCP. Ports `4444` and `4445` were listed as allowed but refused connections; only `9999` was live.
- Files: [`cryptgate`](extracted/cryptgate), [`solve.py`](solve.py)

## Problem Summary

> The Vesper Watch, a guild of vampire-hunters, runs a little check-in kiosk at the mouth of its crypt. Hunters sign the roster on the way in; the kiosk greets them back and, somewhere behind it, keeps a sealed record — the name the Watch has marked for tonight. The kiosk is the only thing exposed. It speaks a plain line protocol over TCP and answers to `gate>`. Most of its commands are routine guild bookkeeping. You have the kiosk program itself, nothing more. The record is the flag, in the form pwnable{...}, chosen per instance.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Vulnerability Class

The exploit chains three issues:

1. **Information disclosure:** `cmd_checkin` writes 128 bytes from a buffer that was cleared and filled for only 64 bytes. The extra output discloses adjacent stack data, including the stack canary. This leak defeats the canary's secrecy.
2. **Stack-based buffer overflow:** `cmd_seal` reads up to 512 bytes into an 80-byte stack buffer. The attacker can overwrite the canary, saved RBP, and return address.
3. **Return-address hijack to a linked function:** the payload restores the leaked canary and replaces the return address with `read_sealed_record`. This is a ret2win-style, ret2known-function exploit. No ROP chain or ret2libc is needed: the non-PIE binary already contains a function that reads and prints the flag file.

## Binary Analysis

The download was `buffy_vampire1.zip`, password `secplayground`. It contained one file, `cryptgate`: a dynamically linked, not-stripped x86-64 ELF. Its SHA-256 was:

```text
57ddb8177207f9973d5c47f76bd55f3a2d4f6b513678c985026023e801117d9a
```

Because the host machine is macOS/arm64 and the binary is amd64 Linux, `checksec` was run in the local `ctf-box` Docker image. It reported:

```text
Partial RELRO
Stack Canary found
NX enabled
No PIE (base 0x400000)
SHSTK enabled
IBT enabled
Not stripped
```

`objdump -d -M intel` showed these commands in the binary: `CHECKIN`, `SEAL`, `ROSTER`, `BADGE <id>`, `LANTERN`, `HELP`, and `QUIT`. The flag file path is `/opt/cryptgate/.roster/record.dat`.

### `main` and `read_line`

`main` at `0x4017d6` runs the command loop. It reads a command into a `0x80`-byte buffer, compares it with the command strings, and calls the matching handler without arguments. The `CHECKIN` and `SEAL` branches use direct calls at the same stack depth; each return address leads back into the dispatch loop, which jumps to its top.

The input helper `read_line(buf, maxlen)` at `0x4012ec` reads one byte at a time using raw `read()` calls. It stops within `maxlen - 1` bytes and null-terminates the buffer. This input path is bounds-checked and is not the bug.

### `cmd_checkin`: stack disclosure

`cmd_checkin` starts at `0x40145b`. Its stack frame reserves `0x50` bytes. The name buffer begins at `rbp-0x50`; the canary is at `rbp-0x8`, which puts it 72 bytes from the start of the buffer.

The handler clears `0x40` bytes with `memset`, then reads at most `0x40` bytes from standard input. Those operations stay within the buffer. The bug follows: after printing `Logged at the gate: `, the handler calls `write(1, buf, 0x80)`. It sends 128 bytes from the buffer even though only the first 64 bytes were cleared or filled.

The 128-byte output exposes this frame layout:

| Offset from buffer | Data |
| ---: | --- |
| `0–63` | Cleared/input name bytes |
| `64–71` | Adjacent stack bytes |
| `72–79` | Stack canary |
| `80–87` | Saved RBP |
| `88–95` | Return address into `main` |

The leaked return address is `0x4018a7` in little-endian form. It matches the instruction immediately after `main` calls `cmd_checkin`, confirming the offset calculation.

### `cmd_seal`: stack overflow

`cmd_seal` starts at `0x4014ed`. It has the same `0x50`-byte stack frame and buffer-to-canary offset as `cmd_checkin`. Both handlers are called from the same depth in `main`'s dispatch loop, so the canary leaked by `CHECKIN` is valid for `SEAL` on the same connection.

After printing `Paste the roster record to seal: `, `cmd_seal` calls `read(0, buf, 0x200)`. That permits up to 512 bytes into the 80-byte stack buffer. There is no check against the buffer size. An input of 96 bytes reaches the saved return address at offset 88.

### `read_sealed_record`: flag-printing function

`read_sealed_record` is at `0x4013a7`. It takes no arguments. It opens `/opt/cryptgate/.roster/record.dat` read-only, reads up to 256 bytes into a stack buffer, writes those bytes to standard output, closes the file, and calls `_exit(0)`.

Normal program flow never calls this function. `SEAL` does not write its input to the record file; its apparent sealing operation is a red herring. The function remains linked into the binary and can be reached by replacing `cmd_seal`'s return address.

## Solution Walkthrough

### 1. Connect to the live service

The challenge listed ports `4444` and `4445` as allowed, but both refused connections. The service answered on TCP port `9999` at `136.85.48.133` and presented the `gate>` prompt.

### 2. Leak the canary with `CHECKIN`

On one TCP connection, send `CHECKIN`, then a short name such as `leak`. Read the 128 bytes written from the handler's buffer after the `Logged at the gate: ` prompt. Calculate offsets from the start of those 128 leaked buffer bytes, not from the start of the full response:

```python
canary = leak[72:80]
saved_rbp = leak[80:88]       # not needed for the payload
leaked_return = leak[88:96]
```

The leaked return address decodes to `0x4018a7` in little-endian order. This confirms that the buffer offsets match the disassembly.

### 3. Overwrite the return address with `SEAL`

Send `SEAL` on the same connection, then send 96 bytes. Preserve the canary, use eight filler bytes for saved RBP, and place `read_sealed_record` at the return-address offset:

```python
read_sealed_record = 0x4013a7
payload = (
    b"B" * 72
    + canary
    + b"C" * 8
    + read_sealed_record.to_bytes(8, "little")
)
```

When `cmd_seal` returns, execution enters `read_sealed_record`. The function reads the per-instance record and prints it to the socket, then exits. No libc address leak is needed because the binary has no PIE and its function addresses are fixed.

The reported `SHSTK` and `IBT` properties did not prevent this return redirection on the live target.

### 4. Observe the solve

The socket response printed:

```text
pwnable{2mAV8zAYvj}
```

The platform score changed from 20 to 30, and the live feed showed `Captured Buffy Vampire#1 +10`. No manual flag submission through the UI was needed. This suggests that the platform validated the solve out of band against the live target.

## Exploit / Script

[`solve.py`](solve.py) is the full solve script. It uses plain Python 3 and the standard-library `socket` module; it does not use pwntools. The payload construction above shows the key overwrite without reproducing the full script.

## Flag

`pwnable{2mAV8zAYvj}`

## Lessons Learned

- A bounded input read does not make a handler safe if a later output call sends more bytes than the buffer contains. Check both read and write lengths.
- Stack canaries detect many overwrites, but an information leak can disclose the canary and let an attacker preserve it.
- A no-PIE binary exposes stable function addresses. If a useful function is already linked in, a direct return-address overwrite can avoid building a ROP chain or using libc.
- Treat dead or unreachable functions as part of the attack surface. `read_sealed_record` was not part of normal flow, but it already performed the needed file read and output.

## References

- [`cryptgate`](extracted/cryptgate)
- [`solve.py`](solve.py)
