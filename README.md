# CTF Writeups

Cybersecurity learning portfolio for CTF practice, event writeups, topic notes, and reusable challenge-analysis templates.

This repository is a personal study archive, but it is organized so another learner, reviewer, or hiring manager can quickly understand what was practiced, how each challenge was approached, and which skills were developed over time.

## Overview

The repo collects capture-the-flag work across event challenges and practice platforms. It is intentionally learning-focused: solved entries should explain the reasoning behind the solution, incomplete entries should be marked clearly, and reusable lessons should be linked back into topic notes.

The main goals are to:

- document practical cybersecurity learning across web, crypto, forensics, OSINT, pwn, reverse engineering, and miscellaneous challenges;
- keep challenge artifacts, solve scripts, notes, and screenshots discoverable;
- show growth from beginner walkthroughs toward repeatable, professional analysis;
- maintain a safe public archive that does not publish private platform content, active challenge secrets, or unauthorized target details.

## Who This Repo Is For

- **Learners:** use the structure, templates, and notes as a study pattern for writing clearer CTF analysis.
- **Reviewers:** browse event and practice indexes to see the range of topics covered.
- **Future me:** revisit old solves, identify weak areas, and improve writeups as techniques become clearer.

This is not intended to be a dump of flags or copy-paste answers. The value is in the method, evidence, and lessons learned.

## Learning Path

Start with [LEARNING_PATH.md](LEARNING_PATH.md). It groups the repo into stages:

1. **Foundations:** shell, Git hygiene, Python basics, file inspection, and writeup habits.
2. **Category fluency:** web, crypto, forensics, OSINT, pwn, and reverse engineering basics.
3. **Professional workflow:** repeatable scripts, clean artifacts, structured reasoning, and references.
4. **Senior-level growth:** compare techniques, extract reusable lessons, and improve old writeups.

Recommended browsing flow:

1. Pick a topic from [notes](notes).
2. Read the related event or practice examples linked from that note.
3. Compare the challenge README with any notebook or solve script.
4. Record reusable lessons back into the relevant topic note.

## Repository Structure

```text
events/
  <year>/<event>/<category>/<challenge>/
practice/
  <platform>/<challenge>/
notes/
  <topic>.md
templates/
  challenge-readme.md
  challenge-writeup.md
  challenge-writeup.ipynb
docs/
  CTF_WRITEUP_GUIDE.md
```

| Area | Purpose |
| --- | --- |
| [events](events) | Writeups from time-boxed CTF events, organized by year, event, category, and challenge |
| [practice](practice) | Platform practice, lab work, and incomplete exercises |
| [notes](notes) | Reusable topic notes and links back to examples |
| [templates](templates) | Starting points for new challenge README and notebook writeups |
| [docs/CTF_WRITEUP_GUIDE.md](docs/CTF_WRITEUP_GUIDE.md) | Quality guide for future writeups |

## Event Index

| Event | Year | Notes |
| --- | --- | --- |
| [TCP1P](events/2024/tcp1p/README.md) | 2024 | Forensics, misc, OSINT, and pwn writeups |
| [LA CTF](events/2025/la-ctf/README.md) | 2025 | Web, crypto, misc, rev, and welcome writeups |
| [STDiOCTF](events/2025/stdioctf/README.md) | 2025 | Unsorted notebook and archive material |
| [Cybersplash](events/2026/cybersplash/README.md) | 2026 | Misc artifacts staged for future writeups |

## Practice Index

| Platform | Notes |
| --- | --- |
| [picoGym](practice/picogym/README.md) | Challenge files, scripts, notebooks, and learning notes |
| [OverTheWire](practice/overthewire/README.md) | Bandit notes and Linux fundamentals practice |
| [SecPlayground](practice/secplayground/README.md) | Web security playground notes |

## Writeup Quality Bar

Each challenge should have a short `README.md` for GitHub browsing. A notebook or separate Markdown writeup can be added when the solve path benefits from commands, scripts, screenshots, or longer reasoning.

A strong writeup should include:

- metadata: event, category, difficulty if known, status, files, and skills learned;
- problem summary: what the challenge provided and what needed to be recovered;
- observations: file types, source snippets, HTTP behavior, crypto parameters, binary protections, or other evidence;
- method: the reasoning path, including false starts when useful;
- reproducibility: commands, scripts, or notebook cells that can be rerun safely;
- lesson: the transferable technique or mistake to remember next time;
- safety: no private platform content, active challenge secrets, or unauthorized targets.

Incomplete entries should be explicit. A short, honest TODO is better than a polished-looking page with missing analysis.

## Status Labels

Use consistent labels so the repo is easy to scan:

| Label | Meaning |
| --- | --- |
| `Solved` | The challenge has a completed solve path and a clear explanation |
| `In progress` | The challenge has meaningful notes but still needs cleanup, verification, or a final explanation |
| `TODO` | The challenge is staged but not meaningfully written up yet |
| `Reference` | The page is a topic note, index, template, or supporting document rather than a challenge solve |

If a challenge has multiple parts, use the lowest honest status until the full page is clear.

## Tooling

Common tools and workflows represented in the repo include:

- shell utilities for file inspection, archives, encodings, and process interaction;
- Python scripts and notebooks for parsing, decoding, brute-force search, and automation;
- browser developer tools and HTTP inspection for web challenges;
- image, audio, archive, packet-capture, and metadata tools for forensics;
- compiler/runtime tooling for pwn and reverse-engineering practice;
- Git and Markdown hygiene for keeping writeups reviewable.

Challenge-specific tools should be documented in the relevant writeup rather than only implied by command history.

## Safe And Legal Note

This repository is for authorized CTFs, practice labs, and intentionally vulnerable training environments only.

Do not use these notes against systems you do not own or do not have permission to test. Avoid publishing active challenge flags, private platform material, personal data, credentials, API keys, tokens, or target details that could harm real systems. When in doubt, redact the sensitive value and explain the technique instead.

## Contributing Notes

This is a personal learning repo, but future entries should follow the standards in [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/CTF_WRITEUP_GUIDE.md](docs/CTF_WRITEUP_GUIDE.md).

Before adding a new writeup:

1. Create a challenge folder using lowercase kebab-case.
2. Start from [templates/challenge-readme.md](templates/challenge-readme.md) or [templates/challenge-writeup.md](templates/challenge-writeup.md).
3. Add a notebook only when it improves reproducibility or explanation.
4. Keep original challenge artifacts separate from generated output.
5. Add links from the event index, practice index, or topic notes when useful.

## Status

Status: active learning portfolio.

Some entries are complete, some are staged for cleanup, and some are intentionally marked TODO. The next improvement pass should focus on normalizing challenge metadata, linking topic notes to examples, and moving unsorted artifacts into challenge-specific folders.
