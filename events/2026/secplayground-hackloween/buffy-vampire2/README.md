# Buffy Vampire#2

## Metadata

- Event: SECPlayground Hackloween CTF 2026
- Category: Pwnable
- Points: 30
- Difficulty: Medium
- Tags: VM, MEDIUM
- Solves: 25 at time of solve
- Status: Solved
- Target: `34.142.133.71:9999` over TCP. Ports `4444` and `4445` were listed as allowed but were not used.
- Files: [`armory`](extracted/armory), [`solve.py`](solve.py)

## Problem Summary

> Deeper inside the Vesper Watch guild-house sits the quartermaster's stake-and-supply ledger. Clerks jot short notes against each entry, and the ledger keeps one sealed requisition with tonight's countersign. The ledger answers to `qm>` over TCP and will read notes back. The program and its exact runtime libraries are provided. Make it emit the sealed requisition: a per-instance `pwnable{...}` flag. Only one internal routine re-emits the requisition, and the menu does not call it. The flag changes each time the challenge is redeployed.

## Prediction
<!-- user fills this in -->

## Solve Log
<!-- user fills this in -->

## Vulnerability Class

The exploit chains three issues:

1. **Format-string vulnerability (CWE-134):** `cmd_note` passes the user-controlled note directly to `printf` as its format string. Positional specifiers such as `%13$p` and `%15$p` read values from variadic argument slots even though the call supplies no real variadic arguments. This out-of-bounds stack read reveals both the stack canary and a return address used to calculate the PIE base. A `%n` specifier could also support writes, but this solve only needed reads.
2. **Stack-based buffer overflow:** `cmd_commit` accumulates raw `read()` calls into an 80-byte stack buffer without checking its size. Sending 96 bytes overwrites the canary, saved RBP, and saved return address.
3. **Return-address hijack to a linked function:** the payload restores the canary and returns into `reissue_sealed_record`, a function present in the binary but absent from normal command dispatch. This is a ret2win, or ret2known-function, chain. It needs no ROP chain or libc leak: only the binary's PIE base must be recovered.

## Binary Analysis

The download was `buffy_vampire2.zip`, with password `secplayground`. It contained `armory`, `libc.so.6`, and `ld-linux-x86-64.so.2`. The prompt explicitly provided the exact runtime libraries. The binary is a dynamically linked, not-stripped x86-64 PIE ELF. The bundled libc is stripped GNU C Library 2.35 (`Ubuntu GLIBC 2.35-0ubuntu3.15`).

Because the host is macOS/arm64 and the binary is amd64 Linux, `checksec` was run in the local `ctf-box` Docker image. It reported:

```text
Partial RELRO
Stack Canary found
NX enabled
PIE enabled
SHSTK enabled
IBT enabled
Not stripped
```

The binary's commands are `ADD <item> <qty>`, `LIST`, `NOTE <text>`, `COMMIT`, `AUDIT`, `EXPORT`, `SEAL`, `HELP`, and `QUIT`. The flag file path is `/opt/armory/.ledger/record.dat`.

All addresses below are static offsets within the PIE image. Add the process's randomized load base to get each runtime address.

### `cmd_note`: format-string leak

`cmd_note` starts at offset `0x17c1`. It clears a 32-byte stack buffer, then copies up to 31 bytes of the supplied note with `strncpy`. Since `strncpy` does not guarantee a null terminator when the source is at least 31 bytes, longer notes can fill the buffer; the probes here are shorter.

After printing `note recorded: `, the handler calls `printf(buf)`. The buffer is the format string, and the call provides no corresponding variadic arguments. Positional probes therefore expose values from the variadic argument registers and stack slots.

Local probes identified these positions:

| Probe | Value |
| --- | --- |
| `NOTE %13$p` | Stack canary; random per process and ends in `00` |
| `NOTE %15$p` | Return address into `main`, equal to PIE base + `0x1d89` |

The return address is the instruction immediately after the call to `cmd_note` at `main` offset `0x1d84`. Subtracting `0x1d89` from the leaked value recovers the PIE base.

### `cmd_commit`: stack overflow

`cmd_commit` starts at offset `0x1865`. It reserves a `0x60`-byte stack frame. The input buffer begins at `rbp-0x50`; the canary sits at `rbp-0x8`. This gives 72 bytes from the buffer start to the canary, followed by saved RBP at offset 80 and the return address at offset 88.

After printing `paste the record line to commit: `, the handler repeatedly calls raw `read()`, accumulating bytes until it has received `0x200` (512) bytes or a read returns EOF/error. It uses the remaining amount as the next read length but does not check the actual buffer size. A short overflow payload leaves the handler waiting for the rest, so the client must half-close its write side after sending the payload. The next read returns zero, and the function proceeds to its epilogue.

### `reissue_sealed_record`: flag-printing function

`reissue_sealed_record` is at offset `0x139f` and takes no arguments. It opens `/opt/armory/.ledger/record.dat` read-only, reads up to 256 bytes into a stack buffer, writes those bytes to standard output, closes the file, and calls `_exit(0)`. If `open()` fails, it calls `_exit(1)`.

The function exists in the binary but normal command dispatch never reaches it, matching the challenge hint. Once the PIE base is known, its runtime address is `PIE base + 0x139f`.

## Solution Walkthrough

### 1. Prepare the local binary

Extract `buffy_vampire2.zip` with password `secplayground`. The archive contains the binary and matching libc and dynamic loader. The binary was analyzed inside the local `ctf-box` Docker image, with its interpreter and library path patched to use the bundled runtime.

The format-string positions were probed locally across multiple runs and checked against disassembly. Position 15 consistently matched the local PIE base plus `0x1d89`; position 13 consistently ended in `00` and varied between runs. A Python `subprocess` harness drove the patched binary over stdin/stdout because `socat` was unavailable in the local toolchain.

The local flag file was absent. A successful redirect therefore ended with `record committed\nrecord unavailable\n` and exit code 1, the function's clean `open()` failure path. This confirmed the canary preservation and return-address overwrite without requiring a working flag file. QEMU user-mode emulation loaded the binary at the same base in these local runs, so local testing validated the exploit mechanism but did not replace the remote PIE leak.

### 2. Leak the canary and PIE base

Connect to `34.142.133.71:9999` and use `NOTE` with positional format specifiers. The solve script reads the canary from position 13 and the return address from position 15:

```text
NOTE %13$p
NOTE %15$p
```

The canary is needed to pass the stack protector check. The return address points to `main` offset `0x1d89`, so subtracting that offset gives this connection's PIE base. Both values were probed and validated locally before use against the live target.

### 3. Redirect `COMMIT` to the reissue routine

Calculate the runtime function address from the leaked base, then build the 96-byte payload:

```python
canary = int(canary_leak, 16)
pie_base = int(return_leak, 16) - 0x1d89
reissue_sealed_record = pie_base + 0x139f

payload = (
    b"A" * 72
    + canary.to_bytes(8, "little")
    + b"C" * 8
    + reissue_sealed_record.to_bytes(8, "little")
)
```

Send `COMMIT`, then the payload. Half-close the socket's write side so the accumulating read loop sees EOF:

```python
sock.sendall(payload)
sock.shutdown(socket.SHUT_WR)
```

When `cmd_commit` returns, execution enters `reissue_sealed_record`. The routine reads and prints the per-instance flag, then exits.

### 4. Observe the live solve

The leak and payload ran over one TCP connection. In one observed run, the return address was `0x563d0659ed89`, the PIE base was `0x563d0659d000`, and `reissue_sealed_record` was `0x563d0659e39f`. These values confirmed that ASLR was active remotely and that the leak was required.

The socket returned:

```text
pwnable{IQJL0BRM5R}
```

The platform score changed from 30 to 60, and the live feed showed `Captured Buffy Vampire#2 +30`. No manual flag submission through the UI was needed. This suggests that the platform validated the solve out of band against the live target.

Buffy Vampire#1 used the same leak-then-overflow-to-dead-function pattern, but its binary had no PIE, so the target address was already static. Buffy Vampire#2 enables PIE and needs the format-string return-address leak to calculate the target address.

## Exploit / Script

[`solve.py`](solve.py) is the full solve script. It uses plain Python 3 and the standard-library `socket` module; it does not use pwntools. The leak and payload snippets above show the key calculations without reproducing the full script.

## Flag

`pwnable{IQJL0BRM5R}`

## Lessons Learned

- A format-string bug can disclose both a stack canary and a PIE return address. Leaking both defeats two separate mitigations.
- A looping read can still overflow a buffer when it has no bound tied to that buffer's size. If the loop waits for a fixed total, half-close the socket to make a short payload proceed.
- PIE randomizes code addresses, but a known return address inside the binary reveals the load base. A useful linked function can then be called directly without a libc leak or ROP chain.
- Local emulation can validate stack layout and control flow while still differing from the live target's ASLR behavior.

## References

- [`armory`](extracted/armory)
- [`solve.py`](solve.py)
