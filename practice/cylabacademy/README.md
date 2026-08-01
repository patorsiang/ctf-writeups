# CyLab Academy

## Summary

CyLab Academy is the new home for structured picoCTF/picoGym-style practice in this repo. Use this area for learning-path challenges, checkpoints, and notes from the platform.

This section is self-guided study. The point is to save what was learned from each challenge clearly enough that future review is easy, without turning the repo into an AI coaching log.

## Folder Layout

```text
practice/cylabacademy/
  README.md
  queue.md
  learning-paths/
    README.md
  challenges/
    <learning-path>/
      <challenge-name>/
        README.md
        attachments/
        output/
        solve.py
        main.ipynb
```

Use lowercase kebab-case for both learning paths and challenge names.

Examples:

```text
practice/cylabacademy/challenges/web-security/cookies/
practice/cylabacademy/challenges/cryptography/mini-rsa/
practice/cylabacademy/challenges/forensics/packet-primer/
```

## New Challenge Workflow

1. Add the challenge to [queue.md](queue.md) before or during the first attempt.
2. Create a folder under `challenges/<learning-path>/<challenge-name>/`.
3. Start from [../../templates/cylabacademy-challenge-readme.md](../../templates/cylabacademy-challenge-readme.md).
4. Put original files in `attachments/` when there is more than one file or when generated output also exists.
5. Put generated files in `output/` only when they help explain or verify the solve.
6. Link the finished or in-progress challenge from [learning-paths/README.md](learning-paths/README.md).

## Status Labels

| Label | Meaning |
| --- | --- |
| `Queued` | Selected from a platform learning path but not started |
| `Attempting` | Active challenge notes exist, but there is no complete solve yet |
| `Solved` | The solve is complete and the reasoning is written clearly |
| `Review` | Solved earlier, but the writeup needs cleanup or better explanation |
| `Skipped` | Intentionally paused because it depends on missing background |

## Legacy picoGym Material

Older picoGym work remains in [../picogym](../picogym). Keep it there unless you are actively cleaning up a specific challenge. New CyLab Academy learning-path work should go in this folder.

When an old picoGym challenge becomes useful for a CyLab Academy path, add a link to it from [learning-paths/README.md](learning-paths/README.md) instead of duplicating files.
