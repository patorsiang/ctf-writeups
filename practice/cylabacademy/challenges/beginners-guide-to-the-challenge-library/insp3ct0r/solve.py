"""Insp3ct0r — harvest a page's client-side source and its comments.

The challenge splits a flag across the three things every web page ships
to the browser: the HTML, a linked stylesheet, and a linked script. All
three are readable by anyone who asks the server for them, which is the
whole point.

Rather than hardcode this one challenge, this is the recon step
generalised: fetch a page, discover its linked assets, fetch those too,
and pull every comment out of each. That is the first move on most
beginner web challenges.

    python3 solve.py http://host:port/          # harvest a live target
    python3 solve.py                            # replay the pinned capture

Stdlib only -- no requests/bs4, so it runs anywhere Python does.
"""

import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

TIMEOUT = 10

# Comment syntaxes, by the file type that uses them. JS and CSS share the
# /* */ block form; only JS has the // line form, and matching // in CSS
# would eat the // in any protocol-relative URL.
HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
BLOCK_COMMENT = re.compile(r"/\*(.*?)\*/", re.DOTALL)
LINE_COMMENT = re.compile(r"(?://)(.*)$", re.MULTILINE)

# Deliberately loose: a fragment like `picoCTF{tru3_d3` has no closing
# brace, so requiring one would miss exactly the case this challenge is
# built around. Used for recon reporting -- "does anything here look like
# a flag" -- not for assembly.
FLAG_HINT = re.compile(r"[a-zA-Z0-9_]*CTF\{[^}]*\}?|flag\{[^}]*\}?", re.IGNORECASE)

# For assembly. Only the *first* third is flag-shaped; parts 2 and 3 are
# bare text (`t3ct1ve_0r_ju5t`, `_lucky?302945a7}`), so matching on flag
# shape would silently drop two thirds of the answer. The comments label
# themselves "N/3", which gives both the payload and its position.
FLAG_PART = re.compile(r"(\d)\s*/\s*3\b.*?flag:\s*(\S+)", re.IGNORECASE | re.DOTALL)


class AssetFinder(HTMLParser):
    """Collect <script src> and <link href> targets.

    Only these two: they are the files the browser is told to go and
    fetch separately, which is what makes them easy to forget to look at.
    """

    def __init__(self):
        super().__init__()
        self.assets: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("src"):
            self.assets.append(attrs["src"])
        elif tag == "link" and attrs.get("href"):
            self.assets.append(attrs["href"])


def find_assets(html: str, base_url: str) -> list[str]:
    """Absolute URLs for every linked script/stylesheet, order preserved,
    duplicates dropped."""
    finder = AssetFinder()
    finder.feed(html)
    seen, out = set(), []
    for ref in finder.assets:
        url = urllib.parse.urljoin(base_url, ref)
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def extract_comments(text: str, kind: str) -> list[str]:
    """Pull comments out of one file. `kind` selects the syntaxes to try,
    because applying JS rules to CSS produces false positives."""
    if kind == "html":
        patterns = [HTML_COMMENT]
    elif kind == "css":
        patterns = [BLOCK_COMMENT]
    elif kind == "js":
        patterns = [BLOCK_COMMENT, LINE_COMMENT]
    else:
        raise ValueError(f"unknown kind {kind!r}; expected html, css or js")

    found = []
    for pattern in patterns:
        found.extend(match.strip() for match in pattern.findall(text))
    return [c for c in found if c]


def kind_for(url: str) -> str:
    path = urllib.parse.urlparse(url).path.lower()
    if path.endswith(".css"):
        return "css"
    if path.endswith(".js"):
        return "js"
    return "html"


def fetch(url: str, timeout: int = TIMEOUT) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def harvest(base_url: str, timeout: int = TIMEOUT) -> dict[str, list[str]]:
    """Fetch the page and everything it links, returning {url: comments}.

    An asset that fails to load is recorded rather than raising -- one
    404 among five assets should not lose the other four.
    """
    html = fetch(base_url, timeout)
    results = {base_url: extract_comments(html, "html")}
    for url in find_assets(html, base_url):
        try:
            body = fetch(url, timeout)
        except Exception as exc:
            results[url] = [f"<fetch failed: {exc}>"]
            continue
        results[url] = extract_comments(body, kind_for(url))
    return results


def flag_fragments(results: dict[str, list[str]]) -> list[str]:
    """Every flag-shaped substring found, in discovery order."""
    out = []
    for comments in results.values():
        for comment in comments:
            out.extend(FLAG_HINT.findall(comment))
    return out


# Recovered from http://fickle-tempest.picoctf.net:56245/ before the
# instance expired. picoCTF spins these down, so the live URL will not
# answer -- the capture is kept so the writeup stays checkable.
CAPTURED = {
    "index.html": "Html is neat. Anyways have 1/3 of the flag: picoCTF{tru3_d3",
    "mycss.css": "You need CSS to make pretty pages. Here's part 2/3 of the flag: t3ct1ve_0r_ju5t",
    "myjs.js": "Javascript sure is neat. Anyways part 3/3 of the flag: _lucky?302945a7}",
}


def assemble(comments=None) -> str:
    """Join labelled flag thirds into the full flag.

    Order comes from each comment's own "N/3" marker, never from the
    order the comments arrived in -- a browser fetches CSS before JS,
    which is not the order the parts concatenate in.

    Raises if the parts are not exactly 1/3, 2/3 and 3/3: a missing or
    duplicated third would otherwise produce a plausible-looking but
    wrong flag, which is worse than an error.
    """
    if comments is None:
        comments = CAPTURED.values()

    parts: dict[int, str] = {}
    for comment in comments:
        match = FLAG_PART.search(comment)
        if not match:
            continue
        index = int(match.group(1))
        if index in parts and parts[index] != match.group(2):
            raise ValueError(f"conflicting values for part {index}/3")
        parts[index] = match.group(2)

    if sorted(parts) != [1, 2, 3]:
        raise ValueError(f"expected parts 1,2,3; found {sorted(parts) or 'none'}")
    return "".join(parts[i] for i in (1, 2, 3))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        results = harvest(sys.argv[1])
        for url, comments in results.items():
            print(f"\n=== {url}")
            for comment in comments:
                print(f"  {comment}")
        fragments = flag_fragments(results)
        if fragments:
            print("\nflag-shaped fragments:", fragments)
    else:
        print("FLAG:", assemble())
