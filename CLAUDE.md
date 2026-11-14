# CLAUDE.md

Repo conventions live in [CONTRIBUTING.md](CONTRIBUTING.md) (Learning Rules) and
[LEARNINGS.md](LEARNINGS.md) (append-only).

## Women TCT 2026 sprint (until 2026-12-26)

Plan: [training/women-tct-2026/README.md](training/women-tct-2026/README.md).

- **At session start:** run `python3 tools/drill_stats.py`. Say in one line if the
  current week is well behind plan, has a week over 20 h, or shows log problems.
- **Registration:** from 2026-11-29, ask "registered yet?" every session until the
  README's "Registered" box is ticked. The deadline is 2026-12-10.
- **Q-track drills (AI allowed):** act as the competition AI. Pair with the user,
  who drives. Agents only take grindy sub-tasks, and only on local files until the
  organizer confirms "AI allowed" covers agents. Log `ai = yes`.
- **F-track drills (no AI):** use `/ctf-hint` escalation only. No flags, no solving.
  Record the hint level (0–3) in the log. Hint ≥ 2 → add a 7-day re-solve.
- **Sunday review:** copy `training/women-tct-2026/weekly/TEMPLATE.md` to
  `weekly/<YYYY>-W<nn>.md` and fill it with the user from `drill_stats.py`.
  Update the README's easy-ready table.
- **Never write the user's Prediction or Solve Log.**
- **Don't install tools without asking.** `tools/check_kit.sh` only reports.
