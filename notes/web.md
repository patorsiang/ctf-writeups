# Web Notes

## Beginner Checklist

- Read HTML, JavaScript, and network requests before guessing.
- Look for client-side secrets, hidden routes, cookies, and weak validation.
- Reproduce requests with a script when manual browser steps become repetitive.

## Client-Side Recon: Read What You Were Already Given

**Everything the browser renders was sent to the browser.** Markup,
styles, scripts and inline config are delivered as source to anyone who
asks. Reading them is not an exploit — it is reading what you were handed.
Minification and obfuscation raise effort, never permission.

### A Page Is Not One File

Loading one URL triggers several requests, and each has its own comment
syntax to check:

| File | Pulled in by | Comments |
| --- | --- | --- |
| the HTML | the address bar | `<!-- ... -->` |
| stylesheets | `<link rel="stylesheet" href>` | `/* ... */` |
| scripts | `<script src>` | `/* ... */` and `//` |
| sourcemaps | `//# sourceMappingURL=…` | hands over *pre-minified* source |

Enumerate the assets; do not stop at the page. Sourcemaps are the biggest
win — a `.map` file often restores original variable names and comments
that minification was assumed to have destroyed.

### view-source vs Elements — Not The Same Thing

| Tool | Shows | Use when |
| --- | --- | --- |
| `view-source:` / `curl` | the **bytes the server sent** | you want ground truth, unmodified by scripts |
| DevTools **Elements** | the **live DOM**, after JS ran | you want the page as it is now |
| DevTools **Sources** / Network | every file fetched | you want the linked CSS/JS |

These disagree on any JS-driven site: a framework builds markup at
runtime, so Elements shows nodes absent from view-source, while a served
HTML comment can be stripped from the DOM. When a challenge says
"inspect", work out which one it means.

Seen in [Insp3ct0r](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/insp3ct0r/README.md),
which splits a flag across HTML, CSS and JS to force checking all three.

### Cheap First Checks On Any Web Target

```bash
curl -s  URL | grep -iE 'flag|todo|secret|key|admin'
curl -sI URL                      # headers: server, cookies, redirects
curl -s  URL/robots.txt           # paths the author wanted hidden
curl -s  URL/sitemap.xml
curl -s  URL/.git/HEAD            # exposed repo -> full source history
```

`solve.py` in the Insp3ct0r folder automates the harvest: fetch a page,
resolve every `<script src>`/`<link href>`, fetch those, and extract each
file's comments by type. Reusable against any target.

### Why This Matters Outside CTFs

Same mechanism, no friendly labelling: API keys hardcoded into frontend
bundles, `//` TODO comments naming internal hostnames, admin endpoints
commented out of the UI but still routed and still live. A secret that
reaches the client is not a secret — it is published.

## Repo Examples

- [CyLab Insp3ct0r](../practice/cylabacademy/challenges/beginners-guide-to-the-challenge-library/insp3ct0r/README.md) — client-side source, comments across HTML/CSS/JS
- [LA CTF lucky-flag](../events/2025/la-ctf/web/lucky-flag/README.md)
- [LA CTF mavs-fan](../events/2025/la-ctf/web/mavs-fan/README.md)
