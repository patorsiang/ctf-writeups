# Contributing and Writeup Standards

This is a personal learning repo, but every entry should be readable by someone else.

## Naming

- Use lowercase kebab-case for folders.
- Use `main.ipynb` for the detailed challenge writeup when analysis benefits from commands, code, screenshots, or incremental notes.
- Use `README.md` for every challenge as a short summary and navigation page.
- Keep original challenge filenames unless renaming would clearly improve clarity.

## Challenge Folder Contents

- `README.md`: short summary, metadata, links, flag, and current status.
- `main.ipynb`: preferred detailed writeup and working analysis notebook.
- Original challenge files: binaries, source, media, archives, captures, documents.
- Solve scripts: small programs used to recover the flag.
- Generated output: keep only if it helps explain or verify the solution.

For new CyLab Academy work, use:

```text
practice/cylabacademy/challenges/<learning-path>/<challenge-name>/
```

Start from [templates/cylabacademy-challenge-readme.md](templates/cylabacademy-challenge-readme.md), and track planned work in [practice/cylabacademy/queue.md](practice/cylabacademy/queue.md).

## Learning Rules

The writeup is how I find out whether I learned something, not just a record
that the challenge got solved.

- **Prediction first.** Before any hint, tool, or AI help, write one line in
  `## Prediction`: "I think this is X because Y." Don't edit it afterward. Score
  it once solved.
- **Solve Log during the solve.** Write `## Solve Log` in my own words while
  working, wrong guesses included. Don't polish it afterward. Claude can help
  tidy the walkthrough, but not the log.
- **Re-solve anything I needed help on.** About 7 days later, redo it cold: no notes,
  no AI, timer running. Track it in the `Re-solve` section of
  [practice/cylabacademy/queue.md](practice/cylabacademy/queue.md). A category
  block only counts as done once its re-solves pass.

## Writeup Rules

- Mark incomplete work as `Status: TODO`.
- For CyLab Academy queue items, use `Queued` before starting and `Attempting` while actively working.
- Do not invent missing points, descriptions, or difficulty.
- Keep flags visible because this is a writeup archive.
- Explain beginner context where useful, then end with the professional takeaway.
- Prefer short, reproducible commands and scripts over vague prose.
- In notebooks, keep cells ordered from observation to solution; avoid leaving unrelated scratch cells in the final writeup.
- If a challenge does not need a notebook, keep the detailed writeup in `README.md` and mark `main.ipynb` as not applicable.
