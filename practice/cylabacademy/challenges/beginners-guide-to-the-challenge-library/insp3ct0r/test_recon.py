"""Tests for Insp3ct0r.

The picoCTF instance is long gone, so testing against the live URL is not
an option. Instead the challenge's *shape* is reproduced as a local
fixture -- an HTML page linking a stylesheet and a script, one flag third
commented into each -- and served over real HTTP from a throwaway server.

That makes these integration tests, not mocks: urllib really speaks HTTP,
the parser really sees bytes off a socket, relative asset paths really
get resolved. A mocked fetch would pass even if find_assets built broken
URLs, which is precisely the bug worth catching.

Run either way:
    python3 test_recon.py
    pytest test_recon.py
"""

import functools
import http.server
import tempfile
import threading
from pathlib import Path

from solve import (
    CAPTURED,
    assemble,
    extract_comments,
    find_assets,
    flag_fragments,
    harvest,
    kind_for,
)

FLAG = "picoCTF{tru3_d3t3ct1ve_0r_ju5t_lucky?302945a7}"

# Mirrors the real challenge: three files, three thirds, and the assets
# referenced by *relative* path so URL joining is exercised for real.
INDEX_HTML = """<!doctype html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="mycss.css">
</head>
<body>
  <h1>Inspect Me</h1>
  <!-- Html is neat. Anyways have 1/3 of the flag: picoCTF{tru3_d3 -->
  <script src="myjs.js"></script>
</body>
</html>
"""

MYCSS = """body { background: #fff; }
/* You need CSS to make pretty pages. Here's part 2/3 of the flag: t3ct1ve_0r_ju5t */
"""

MYJS = """function nothing() { return 0; }
/* Javascript sure is neat. Anyways part 3/3 of the flag: _lucky?302945a7} */
"""


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def _serve(directory):
    """Start a real HTTP server on an ephemeral port; return (url, stop)."""
    handler = functools.partial(_QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return f"http://{host}:{port}/index.html", server.shutdown


def _fixture(tmp):
    root = Path(tmp)
    (root / "index.html").write_text(INDEX_HTML)
    (root / "mycss.css").write_text(MYCSS)
    (root / "myjs.js").write_text(MYJS)
    return root


# --------------------------------------------------------------------------
# End-to-end against a real HTTP server
# --------------------------------------------------------------------------


def test_harvest_finds_all_three_files_over_http():
    with tempfile.TemporaryDirectory() as tmp:
        url, stop = _serve(_fixture(tmp))
        try:
            results = harvest(url)
        finally:
            stop()

    assert len(results) == 3, f"expected page + 2 assets, got {list(results)}"
    assert any(u.endswith("mycss.css") for u in results)
    assert any(u.endswith("myjs.js") for u in results)


def test_harvested_comments_assemble_to_the_flag():
    """The full pipeline: HTTP -> parse -> comments -> assembled flag."""
    with tempfile.TemporaryDirectory() as tmp:
        url, stop = _serve(_fixture(tmp))
        try:
            results = harvest(url)
        finally:
            stop()

    all_comments = [c for comments in results.values() for c in comments]
    assert assemble(all_comments) == FLAG


def test_only_the_first_third_is_flag_shaped():
    """Why assembly keys off the N/3 marker rather than flag shape:
    parts 2 and 3 are bare text and a flag regex finds neither."""
    with tempfile.TemporaryDirectory() as tmp:
        url, stop = _serve(_fixture(tmp))
        try:
            results = harvest(url)
        finally:
            stop()

    assert flag_fragments(results) == ["picoCTF{tru3_d3"]


def test_missing_asset_does_not_lose_the_others():
    """A 404 on one asset must not abort the harvest -- partial recon
    beats no recon."""
    with tempfile.TemporaryDirectory() as tmp:
        root = _fixture(tmp)
        (root / "myjs.js").unlink()
        url, stop = _serve(root)
        try:
            results = harvest(url)
        finally:
            stop()

    assert len(results) == 3
    js = next(v for k, v in results.items() if k.endswith("myjs.js"))
    assert js and js[0].startswith("<fetch failed"), js
    assert any("t3ct1ve_0r_ju5t" in c for cs in results.values() for c in cs)


# --------------------------------------------------------------------------
# The pinned capture
# --------------------------------------------------------------------------


def test_captured_fragments_assemble_to_the_flag():
    assert assemble() == FLAG


def test_assemble_ignores_arrival_order():
    """Order comes from the N/3 marker, not from insertion order -- a
    browser loads CSS before JS, which is not the concatenation order."""
    reversed_order = [CAPTURED[k] for k in ("myjs.js", "index.html", "mycss.css")]
    assert assemble(reversed_order) == FLAG


def test_assemble_refuses_an_incomplete_set():
    """Two thirds must not silently concatenate into a wrong-looking
    flag -- a missing part is an error, not a shorter answer."""
    try:
        assemble([CAPTURED["index.html"], CAPTURED["myjs.js"]])
        assert False, "expected ValueError for a missing third"
    except ValueError:
        pass


def test_assemble_detects_conflicting_parts():
    conflicting = [
        CAPTURED["index.html"],
        CAPTURED["mycss.css"],
        CAPTURED["myjs.js"],
        "part 2/3 of the flag: something_else",
    ]
    try:
        assemble(conflicting)
        assert False, "expected ValueError for conflicting part 2"
    except ValueError:
        pass


# --------------------------------------------------------------------------
# Parsing units
# --------------------------------------------------------------------------


def test_find_assets_resolves_relative_paths():
    html = '<link href="css/a.css"><script src="/js/b.js"></script>'
    assets = find_assets(html, "http://x.test/sub/page.html")
    assert assets == ["http://x.test/sub/css/a.css", "http://x.test/js/b.js"]


def test_find_assets_drops_duplicates_but_keeps_order():
    html = '<script src="a.js"></script><script src="a.js"></script><script src="b.js"></script>'
    assert find_assets(html, "http://x.test/") == ["http://x.test/a.js", "http://x.test/b.js"]


def test_css_does_not_use_line_comment_rules():
    """Applying JS's // rule to CSS would swallow the rest of any line
    containing a protocol-relative URL."""
    css = "a { background: url(//cdn.test/i.png); } /* real comment */"
    assert extract_comments(css, "css") == ["real comment"]


def test_js_finds_both_comment_styles():
    js = "// line one\n/* block one */\n"
    assert sorted(extract_comments(js, "js")) == ["block one", "line one"]


def test_kind_is_chosen_by_extension():
    assert kind_for("http://x.test/a/b.css") == "css"
    assert kind_for("http://x.test/a/b.js?v=2") == "js"
    assert kind_for("http://x.test/") == "html"


def test_extract_comments_rejects_unknown_kind():
    try:
        extract_comments("x", "php")
        assert False, "expected ValueError for an unknown kind"
    except ValueError:
        pass


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
