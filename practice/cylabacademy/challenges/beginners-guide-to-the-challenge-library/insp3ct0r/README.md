# Insp3ct0r

## Metadata

- Platform: CyLab Academy / picoCTF (picoCTF 2019, by zaratec/danny)
- Learning Path: The Beginner's Guide to the Challenge Library
- Category: Web Exploitation
- Difficulty: Easy
- Status: Solved
- Started: 2026-08-09
- Completed: 2026-08-09
- Target: `http://fickle-tempest.picoctf.net:56245/` (instance expired)
- Files: `solve.py`, `test_recon.py`
- Skills Learned: view-source, DevTools Elements vs Sources, client-side secrets, asset enumeration

## Problem Summary

> Kishor Balan tipped us off that the following code may need inspection:
> `http://fickle-tempest.picoctf.net:56245/`

The flag is split into thirds and hidden in comments across the three
files the page ships to the browser.

## First Observations

A web page is not one file. Loading this one causes the browser to make
**three** requests:

| Request | Why | Comment syntax |
| --- | --- | --- |
| `index.html` | typed in the address bar | `<!-- ... -->` |
| `mycss.css` | pulled in by `<link rel="stylesheet">` | `/* ... */` |
| `myjs.js` | pulled in by `<script src>` | `/* ... */` and `//` |

The flag is split one third per file, which is the challenge forcing you
to check all three rather than stopping at the first hit.

## Key Idea

**Everything the browser renders was sent to the browser.** HTML, CSS and
JavaScript are delivered as source to anyone who asks the server for them.
Reading them is not an exploit — it is reading what you were handed.

Two mechanics worth separating, because juniors conflate them and it
matters later:

| Tool | Shows | Use when |
| --- | --- | --- |
| `view-source:` / `curl` | the **original bytes the server sent** | you want ground truth, unmodified by scripts |
| DevTools **Elements** | the **live DOM**, after JavaScript has run | you want the page as it is now |
| DevTools **Sources**/Network | every file fetched, including assets | you want the linked CSS/JS |

These can disagree. A JS framework builds its markup at runtime, so
Elements shows nodes that appear nowhere in view-source; conversely a
comment in the served HTML may be stripped from the DOM. When a challenge
says "inspect", ask *which* of the two it means.

## Solution Walkthrough

Browser route (what was actually done):

1. Right-click → **View Page Source** (or `Ctrl/Cmd+U`) on the landing page:

   ```html
   <!-- Html is neat. Anyways have 1/3 of the flag: picoCTF{tru3_d3 -->
   ```

2. DevTools → **Sources**, open `mycss.css`:

   ```css
   /* You need CSS to make pretty pages. Here's part 2/3 of the flag: t3ct1ve_0r_ju5t */
   ```

3. Same panel, `myjs.js`:

   ```js
   /* Javascript sure is neat. Anyways part 3/3 of the flag: _lucky?302945a7} */
   ```

4. Concatenate in `1/3, 2/3, 3/3` order.

Terminal route — faster, scriptable, no clicking:

```bash
curl -s http://host:port/           | grep -i 'flag'
curl -s http://host:port/mycss.css  | grep -i 'flag'
curl -s http://host:port/myjs.js    | grep -i 'flag'
```

## Commands Or Script

[`solve.py`](solve.py) generalises the recon step rather than hardcoding
this challenge: fetch a page, discover every `<script src>` and
`<link href>`, fetch those too, and extract the comments from each
according to its file type.

```bash
python3 solve.py http://host:port/    # harvest a live target
python3 solve.py                      # replay the pinned capture
```

```text
FLAG: picoCTF{tru3_d3t3ct1ve_0r_ju5t_lucky?302945a7}
```

Stdlib only (`urllib`, `html.parser`, `re`) so it runs anywhere.

[`test_recon.py`](test_recon.py) — 14 tests. The picoCTF instance is gone,
so rather than mocking, the tests **reproduce the challenge's shape as a
local fixture and serve it over real HTTP** from a throwaway
`ThreadingHTTPServer` on an ephemeral port:

```bash
python3 test_recon.py    # or: pytest test_recon.py
```

That choice is deliberate. A mocked `fetch` would pass even if
`find_assets` built broken URLs — which is exactly the bug worth catching,
since relative-path resolution is the fiddly part. Real HTTP means
`urllib` really speaks the protocol and relative hrefs really get joined.

Also covered: a 404 on one asset must not abandon the others; assembly
must reject an incomplete or self-contradicting set of thirds rather than
returning a plausible wrong flag.

### A bug the tests caught

The first version extracted fragments with a flag-shaped regex
(`picoCTF\{...`). It crashed, because **only the first third is
flag-shaped** — parts 2 and 3 are bare text (`t3ct1ve_0r_ju5t`,
`_lucky?302945a7}`). Assembly now keys off each comment's own `N/3`
marker, which yields both the payload and its position. Ordering by the
marker also means a browser fetching CSS before JS cannot scramble the
result.

## Flag

```text
picoCTF{tru3_d3t3ct1ve_0r_ju5t_lucky?302945a7}
```

## Lessons Learned

- **Client-side is not secret.** Anything shipped to a browser — markup,
  styles, scripts, inline config — is readable by every visitor.
  Minification and obfuscation raise effort, never permission.
- **This is how real credentials leak.** API keys hardcoded in frontend
  bundles, `//` TODO comments naming internal hosts, admin endpoints
  commented out but still routed. Same mechanism as this challenge,
  without the friendly labelling.
- **Enumerate assets, don't just read the page.** The HTML is one of
  several files. `<script src>`, `<link href>`, and `.map` sourcemaps are
  all fetchable, and sourcemaps in particular can hand over original
  pre-minified source including comments.
- **Elements ≠ view-source.** Live DOM after JS versus the bytes the
  server sent. Check both; they diverge on any modern site.
- **Other cheap first checks** on a beginner web target: `robots.txt`,
  `/.git/` exposure, `sitemap.xml`, cookies, and response headers
  (`curl -I`).

## Follow-Up

- Added the client-side recon checklist to
  [../../../../../notes/web.md](../../../../../notes/web.md).
- `solve.py` is reusable against any future web target — the harvest step
  is the same on most beginner web challenges.
