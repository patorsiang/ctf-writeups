#!/bin/sh
HOST="http://34.158.35.47"
KEY="hearth-porch-6d13"
JAR="$(dirname "$0")/cookies5.txt"
rm -f "$JAR"

echo "== open fresh session =="
OPEN=$(curl -sS -m 15 -c "$JAR" -H "X-Hearth-Key: $KEY" "$HOST/api/v1/hearth/open")
echo "$OPEN"
NONCE=$(echo "$OPEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['nonce'])")
echo "nonce=$NONCE"

python3 -c "
import hashlib
nonce='$NONCE'; key='$KEY'
nk = hashlib.sha256((nonce+':'+key).encode()).hexdigest()
kn = hashlib.sha256((key+':'+nonce).encode()).hexdigest()
print('nk16', nk[:16]); print('nk64', nk)
print('kn16', kn[:16]); print('kn64', kn)
"

try() {
  echo "-- $1 --"; shift
  curl -sS -m 10 -b "$JAR" -i -X POST -H "X-Hearth-Key: $KEY" -H "Content-Type: application/json" "$@" "$HOST/api/v1/hearth/turn" | tail -8
  echo
}

NK16=$(python3 -c "import hashlib; print(hashlib.sha256(('$NONCE:$KEY').encode()).hexdigest()[:16])")
NK64=$(python3 -c "import hashlib; print(hashlib.sha256(('$NONCE:$KEY').encode()).hexdigest())")
KN16=$(python3 -c "import hashlib; print(hashlib.sha256(('$KEY:$NONCE').encode()).hexdigest()[:16])")
KN64=$(python3 -c "import hashlib; print(hashlib.sha256(('$KEY:$NONCE').encode()).hexdigest())")

try "nk16" -d "{\"turn\":\"$NK16\",\"nonce\":\"$NONCE\"}"
try "nk64" -d "{\"turn\":\"$NK64\",\"nonce\":\"$NONCE\"}"
try "kn16" -d "{\"turn\":\"$KN16\",\"nonce\":\"$NONCE\"}"
try "kn64" -d "{\"turn\":\"$KN64\",\"nonce\":\"$NONCE\"}"
