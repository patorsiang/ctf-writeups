#!/bin/sh
# Report which competition-kit tools are present. Never installs anything.
# Exit 0 = all present, 1 = something missing. See training/women-tct-2026/kit.md.

KIT_PY="${KIT_VENV:-$HOME/.venvs/ctf}/bin/python"
[ -x "$KIT_PY" ] || KIT_PY=python3
KIT_DIR="${KIT_DIR:-$HOME/ctf-kit}"
missing=0

ok()   { echo "ok $1"; }
miss() { echo "MISSING $1 ($2)"; missing=1; }

bin() {  # bin <command> <category>
  if command -v "$1" >/dev/null 2>&1; then ok "$1"; else miss "$1" "$2"; fi
}
app() {  # app <name pattern> <label> <category>
  if ls /Applications 2>/dev/null | grep -qi "$1"; then ok "$2"; else miss "$2" "$3"; fi
}
mod() {  # mod <python module> <category>
  if "$KIT_PY" -c "import $1" >/dev/null 2>&1; then ok "py:$1"; else miss "py:$1" "$2"; fi
}
path() {  # path <file or dir> <label> <category>
  if [ -e "$1" ]; then ok "$2"; else miss "$2" "$3"; fi
}

echo "python: $KIT_PY"
bin curl web;        app burp "Burp Suite" web;   bin ffuf web
bin file forensics;  bin strings forensics;       bin exiftool forensics
bin binwalk forensics; bin foremost forensics;    bin vol forensics
bin ghidraRun re-pwn; bin docker re-pwn
bin tshark network
bin jadx mobile;     bin apktool mobile
mod pwn programming
mod Crypto crypto;   mod sympy crypto;            mod gmpy2 crypto
bin steghide misc;   bin zsteg misc
path "$KIT_DIR/cyberchef" "cyberchef-offline" misc
path "$KIT_DIR/wordlists/rockyou.txt" "rockyou" web

exit $missing
