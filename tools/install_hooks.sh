#!/usr/bin/env bash
# Install the versioned git hooks next to the existing Git LFS hooks.
# Does not touch core.hooksPath (that would switch the LFS hooks off).
set -euo pipefail
repo="$(git rev-parse --show-toplevel)"
dest="$(cd "$repo" && git rev-parse --git-path hooks)/pre-commit"
case "$dest" in /*) ;; *) dest="$repo/$dest";; esac
src="$repo/githooks/pre-commit"

if [ -e "$dest" ] && ! grep -q "secret-scan pre-commit hook" "$dest"; then
  echo "refusing: $dest already exists and is not the secret-scan hook. Merge it by hand." >&2
  exit 1
fi
mkdir -p "$(dirname "$dest")"
ln -sf "$src" "$dest"
echo "installed: $dest -> $src"
