# Programming Notes

## Triage playbook (easy, ≤1 page)

Fill from drills — each new line must cite the drill that taught it.

First look at a "solve N rounds over nc" challenge (tools checked by `tools/check_kit.sh`):

- `nc host port` by hand once: read the exact prompt format and the round count.
- Script it with pwntools: `r = remote(host, port)`, `r.recvuntil(b"...")`, `r.sendline(...)`, loop over the rounds, `r.interactive()` at the end.
- `context.log_level = "debug"` while the parser is still wrong.
- Parse with a strict regex on the prompt line, and fail loudly when it doesn't match.

## Repo Examples
