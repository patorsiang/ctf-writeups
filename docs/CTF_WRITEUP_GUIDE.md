# CTF Writeup Guide

This guide defines how future CTF writeups should be added to this repository. The goal is to keep the repo useful as a learning portfolio without turning it into a raw flag dump or an unsafe archive.

## Guiding Principles

- Explain the method, not only the answer.
- Keep the solve path reproducible with commands, scripts, screenshots, or notebook cells when useful.
- Be honest about incomplete work.
- Do not publish private platform content, active challenge secrets, credentials, tokens, or unauthorized target details.
- Prefer concise analysis over long terminal transcripts.

## Recommended Challenge Structure

```text
<challenge>/
  README.md
  main.ipynb          # optional, for longer analysis
  solve.py           # optional, if a script was used
  attachments/       # optional, original challenge files
  output/            # optional, generated files worth keeping
```

Keep original challenge files separate from generated output whenever possible.

## README Sections

Each challenge `README.md` should include:

- **Metadata:** event, category, difficulty if known, status, files, and skills learned.
- **Problem Summary:** what was provided and what the challenge asked for.
- **Observations:** evidence that shaped the solve path.
- **Key Idea:** the main vulnerability, trick, encoding, or investigation pivot.
- **Solution Walkthrough:** steps that another learner can follow.
- **Script Or Commands:** links to scripts or short command snippets.
- **Lessons Learned:** one or more transferable takeaways.
- **References:** docs, papers, or writeups that materially helped.

Use [templates/challenge-readme.md](../templates/challenge-readme.md) or [templates/challenge-writeup.md](../templates/challenge-writeup.md) as the starting point.

For CyLab Academy learning-path work, use [templates/cylabacademy-challenge-readme.md](../templates/cylabacademy-challenge-readme.md) and save challenges under:

```text
practice/cylabacademy/challenges/<learning-path>/<challenge>/
```

## Notebook Guidance

Use `main.ipynb` when the analysis benefits from incremental cells, rich output, plots, screenshots, or exploratory scripts.

Before committing a notebook:

- order cells from observation to conclusion;
- remove unrelated scratch cells;
- avoid large embedded outputs unless they help explain the result;
- use Markdown cells to explain why each step matters;
- keep generated files in a named folder if they are needed for verification.

## Status Labels

Use these labels consistently:

| Label | Meaning |
| --- | --- |
| `Solved` | Complete solve path and explanation |
| `In progress` | Useful notes exist, but the writeup still needs cleanup or verification |
| `TODO` | Staged challenge with little or no analysis yet |
| `Reference` | Supporting note, template, or index page |

CyLab Academy learning-path work may also use `Queued`, `Attempting`, `Review`, and `Skipped` as defined in [practice/cylabacademy/README.md](../practice/cylabacademy/README.md).

Do not mark a challenge `Solved` until the writeup explains the reasoning clearly enough for another learner to follow.

## Quality Checklist

Before opening a documentation PR, check:

- The challenge is linked from the relevant event, practice, or topic index.
- The status label is honest.
- The README explains the reasoning, not just the final command.
- Commands are safe to rerun in a local challenge directory.
- Scripts use placeholder values for credentials, hosts, or tokens.
- Private content, active flags, and sensitive values are not exposed.
- Large generated files are either justified or left out.
- The final lesson is specific enough to reuse.

## Safety And Legal Boundaries

Only document work from authorized CTFs, practice labs, and intentionally vulnerable environments.

For public writeups:

- avoid active challenge flags while an event is live;
- do not include credentials, API keys, tokens, private keys, or service accounts;
- redact private hostnames, IPs, cookies, and session values unless they are challenge-provided and safe to share;
- avoid instructions that target real third-party systems;
- explain sensitive techniques in the context of the lab or challenge.

If a writeup needs to mention a sensitive value, replace it with a placeholder and explain what role the value played.

## Portfolio Standard

A portfolio-ready writeup should show:

- the problem-solving process;
- the technical concept learned;
- evidence that the result was verified;
- a clear boundary between challenge artifacts and generated work;
- a professional note on safety, scope, or assumptions when relevant.

The best writeups make it easy to see both technical growth and judgment.
