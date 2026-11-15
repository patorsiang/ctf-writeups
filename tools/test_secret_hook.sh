#!/usr/bin/env bash
# Tests for the gitleaks pre-commit hook (githooks/pre-commit + tools/install_hooks.sh).
# Runs in throwaway repos; needs gitleaks on PATH. Fake secrets are built at runtime
# so this file itself never contains one.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pass=0; fail=0
check() { if eval "$2"; then echo "ok   $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }

fake_pat() { python3 -c 'import secrets,string;a=string.ascii_letters+string.digits;print("gh"+"p_"+"".join(secrets.choice(a) for _ in range(36)))'; }

new_repo() {  # new_repo <dir>: a git repo with the hook installed
  git init -q "$1" && git -C "$1" config user.email t@example.invalid && git -C "$1" config user.name t
  mkdir -p "$1/githooks" "$1/tools"
  cp "$ROOT/githooks/pre-commit" "$1/githooks/" && cp "$ROOT/tools/install_hooks.sh" "$1/tools/"
  (cd "$1" && bash tools/install_hooks.sh >/dev/null)
}
commit() { git -C "$1" add -A && git -C "$1" commit -qm test >/dev/null 2>&1; }

t="$(mktemp -d)"; trap 'rm -rf "$t"' EXIT

new_repo "$t/a"; echo "hello" > "$t/a/notes.md"
check "clean commit passes"                  'commit "$t/a"'

echo "token = $(fake_pat)" > "$t/a/solve.py"
check "token-shaped string is blocked"       '! commit "$t/a"'

fp="$(cd "$t/a" && gitleaks git --staged --no-banner --redact -f json -r - 2>/dev/null | python3 -c "import json,sys;print(json.load(sys.stdin)[0][\"Fingerprint\"])")"
printf '# fake CTF data\n%s\n' "$fp" > "$t/a/.gitleaksignore"
check "fingerprint in .gitleaksignore allows that one finding" 'commit "$t/a"'

echo "other = $(fake_pat)" > "$t/a/other.py"
check "allowlist does not cover a new secret" '! commit "$t/a"'
git -C "$t/a" reset -q && rm "$t/a/other.py"

new_repo "$t/b"; echo "k = $(fake_pat)" > "$t/b/x.py"
check "fails closed when gitleaks is missing" '! (cd "$t/b" && git add -A && PATH=/usr/bin:/bin git commit -qm t >/dev/null 2>&1)'

new_repo "$t/c"; printf '#!/bin/sh\necho mine\n' > "$t/c/.git/hooks/pre-commit"
check "installer refuses to replace someone else's pre-commit" '! (cd "$t/c" && bash tools/install_hooks.sh >/dev/null 2>&1)'
check "installer is idempotent"              '(cd "$t/a" && bash tools/install_hooks.sh >/dev/null)'
printf '#!/bin/sh\ngit lfs pre-push "$@"\n' > "$t/a/.git/hooks/pre-push"
(cd "$t/a" && bash tools/install_hooks.sh >/dev/null)
check "installer leaves core.hooksPath unset" '! git -C "$t/a" config --get core.hooksPath >/dev/null'
check "installer keeps the LFS pre-push hook" 'grep -q "git lfs pre-push" "$t/a/.git/hooks/pre-push"'

echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
