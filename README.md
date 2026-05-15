# CTF Writeups

This repository is my CTF learning archive. It is organized to be useful while I am learning the basics, but written and structured like a professional portfolio.

## How to Use This Repo

- Start with [LEARNING_PATH.md](LEARNING_PATH.md) to choose what to study next.
- Browse solved event challenges under [events](events).
- Use [practice](practice) for training material and incomplete experiments.
- Read reusable topic notes under [notes](notes).
- Use [templates/challenge-writeup.ipynb](templates/challenge-writeup.ipynb) before adding a new notebook writeup.

## Repository Structure

```text
events/
  <year>/<event>/<category>/<challenge>/
practice/
  <platform>/<challenge>/
notes/
  <topic>.md
templates/
  challenge-writeup.ipynb
  challenge-readme.md
```

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
| [OverTheWire](practice/overthewire/README.md) | Bandit notes and keys |
| [SecPlayground](practice/secplayground/README.md) | Web security playground notes |

## Writeup Quality Bar

The preferred detailed writeup format is `main.ipynb`. Each challenge should also have a short `README.md` so the repo stays easy to browse on GitHub.

A good notebook writeup should explain the reasoning, not only the answer. It should make it clear:

- what the challenge was asking for;
- what signals led to the solution;
- what tools or techniques were used;
- what mistake or lesson should be remembered next time;
- which files are challenge artifacts, solve scripts, or generated output.

Incomplete writeups should be marked `Status: TODO` instead of being silently empty.
