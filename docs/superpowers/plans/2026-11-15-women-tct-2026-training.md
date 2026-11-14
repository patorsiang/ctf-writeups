# Women TCT 2026 Training System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the repo into a measured two-track training system for the Women Thailand Cyber Top Talent 2026 WOpen tier (qualifier 2026-12-12 with AI, final 2026-12-26 without AI).

**Architecture:** A `training/women-tct-2026/` folder holds the plan, the drill log, the kit and the mock and weekly-review files. One stdlib-only Python script, `tools/drill_stats.py`, turns the drill log into the numbers the Sunday review needs. A shell script, `tools/check_kit.sh`, verifies the toolkit offline. A root `CLAUDE.md` tells future sessions how to behave during the sprint.

**Tech Stack:** Markdown. Python 3.14 stdlib only (`unittest`, no pytest: it isn't installed, and the kit must not depend on extra packages for its own tooling). POSIX shell.

**Spec:** `docs/superpowers/specs/2026-11-14-women-tct-2026-training-design.md`

## Global Constraints

- Dates (Asia/Bangkok): qualifier mock **2026-12-05** (7 h, AI allowed); qualifier **2026-12-12 09:00–16:00**; final mock **2026-12-19** (6 h, no AI); final **2026-12-26 09:00–15:00**; register by **2026-12-01** (deadline 2026-12-10).
- Weeks: W1 11-15→11-21, W2 11-22→11-28, W3 11-29→12-05, W4 12-06→12-11, W5–6 12-13→12-25.
- The 9 categories, spelled exactly like this everywhere (log, script, notes): `web`, `forensics`, `re-pwn`, `network`, `mobile`, `programming`, `crypto`, `misc`, `ai-iot`.
- Time boxes: easy 30 min, medium 60 min.
- Weekly budget is 10–15 h. W2–W3 may go over. Anything over **20 h** gets flagged.
- Keep the existing conventions: CONTRIBUTING.md Learning Rules, LEARNINGS.md append-only, kebab-case folders.
- Don't install anything without asking the user first. `check_kit.sh` only reports.
- Don't add a Claude-written Solve Log; the Solve Log is the user's own.

## Review Focus

1. **Hand-edited log rows with sloppy formatting** (extra spaces, `Yes`/`yes`, `25m` vs `25`, an empty time) are expected to be counted, not crash the stats or vanish silently. Malformed rows are reported by line number. Test: `test_tolerates_messy_rows`.
2. **Category typos** (`Web`, `forensic`) are expected to be reported, not counted as a 10th category. Test: `test_unknown_category_reported`.
3. **A solve with AI or with a hint** must not count toward "easy-ready", because the final is no-AI. Test: `test_easy_ready_requires_unassisted`.
4. **Overrun drills** (solved in 45 min on a 30-min box) must not count as easy-ready. Test: `test_easy_ready_requires_within_box`.
5. **An empty log** (day 1) is expected to print all 9 categories as not ready, not error. Test: `test_empty_log`.

---

### Task 1: Training folder skeleton

**Files:**
- Create: `training/women-tct-2026/README.md`, `training/women-tct-2026/drill-log.md`, `training/women-tct-2026/weekly/TEMPLATE.md`, `training/women-tct-2026/mocks/2026-12-05-qualifier-mock.md`, `training/women-tct-2026/mocks/2026-12-19-final-mock.md`

**Interfaces:**
- Produces: the `drill-log.md` table format that Task 2 parses. Header (exact):
  `| date | challenge | category | source | track | box | taken | solved | ai | hint | note |`
  - `date` = `YYYY-MM-DD`
  - `category` = one of the 9 slugs
  - `track` = `Q` or `F`
  - `box` and `taken` = minutes as an integer
  - `solved` and `ai` = `yes`/`no`
  - `hint` = 0–3 (0 = none; 1 = nudge; 2 = technique; 3 = solve path)

- [ ] **Step 1: Write `README.md`.** Copy the spec's Intent, the event table, Goals 1–5, the schedule table, and the registration line with ☐. Add an **Easy-ready** table (9 rows, filled by `drill_stats.py` output at each Sunday review) and links to the log, kit, mocks and weekly folder. No content beyond the spec.
- [ ] **Step 2: Write `drill-log.md`.** A one-paragraph legend of the columns and the hint scale, the header row, the separator, and no data rows.
- [ ] **Step 3: Write `weekly/TEMPLATE.md`.** Sections: `Hours (from drill_stats)`, `Easy-ready changes`, `What the log says`, `Next week: categories + drill count`, `Over 20 h? what gets cut`.
- [ ] **Step 4: Write the two mock files.** Sections: rules for that mock (AI yes/no, 7 h or 6 h, source event to replay), `Board triage (first 15 min)`, a per-challenge table in the drill-log format, `Score / solves`, `Gaps → next week`.
- [ ] **Step 5: Verify.** Run `ls -R training/women-tct-2026`. Expected: the 5 files. Run `grep -c '|' training/women-tct-2026/drill-log.md`. Expected: 2 (header + separator).
- [ ] **Step 6: Commit.** `git add training && git commit -m "feat(training): add Women TCT 2026 training skeleton"`

### Task 2: `drill_stats.py`, which turns the log into review numbers

**Files:**
- Create: `tools/drill_stats.py`, `tools/test_drill_stats.py`

**Interfaces:**
- Consumes: the drill-log format from Task 1.
- Produces:
  - `CATEGORIES: tuple[str, ...]`: the 9 slugs, in Global Constraints order.
  - `@dataclass Drill(date: datetime.date, challenge: str, category: str, track: str, box: int, taken: int, solved: bool, ai: bool, hint: int)`
  - `parse_log(text: str) -> tuple[list[Drill], list[str]]`: drills plus problem messages (`"line N: ..."`).
  - `week_of(d: date) -> str`: the sprint week label (`"W1"`…`"W6"`, `"pre"` before 11-15).
  - `hours_by_week(drills) -> dict[str, float]`
  - `easy_ready(drills) -> dict[str, bool]`: every category key is present. True if at least one drill has `box <= 30`, `solved`, `not ai`, `hint == 0` and `taken <= box`.
  - CLI: `python3 tools/drill_stats.py [path]` (default `training/women-tct-2026/drill-log.md`) prints hours per week (with `OVER 20h` where needed), the easy-ready table, and the problems.

- [ ] **Step 1: Write failing tests in `tools/test_drill_stats.py`** (unittest, using inline log strings):
  - `test_parses_valid_row`: one row → one `Drill` with the exact fields and no problems.
  - `test_tolerates_messy_rows`: `| 2026-11-16 | x | web | pico | Q | 30 | 25m | Yes |  no | 0 | |` parses (taken=25, solved=True). A row missing columns produces `"line N:"` in the problems.
  - `test_unknown_category_reported`: `forensic` → drill excluded; the problem mentions `forensic`.
  - `test_week_of_boundaries`: 11-14→`pre`, 11-15→`W1`, 11-21→`W1`, 11-22→`W2`, 12-12→`W4`, 12-13→`W5`, 12-25→`W6`.
  - `test_hours_by_week`: 3 drills of 60 + 30 min in W1 + 90 min in W2 → `{"W1": 1.5, "W2": 1.5}`.
  - `test_easy_ready_requires_unassisted`: solved easy with `ai=yes` → False; `hint=1` → False.
  - `test_easy_ready_requires_within_box`: taken 45, box 30 → False.
  - `test_empty_log`: header only → 9 keys, all False, no problems.
- [ ] **Step 2: Run** `python3 -m unittest tools/test_drill_stats.py -v`. Expected: errors (module missing).
- [ ] **Step 3: Implement `tools/drill_stats.py`.** Read only table rows after the header line, and normalize cells with `.strip().lower()` and a trailing `m` removed. W5 covers 12-13→12-19 and W6 covers 12-20→12-25 (the spec's W5–6 split into two weeks so the hours stay readable). Anything after 12-25 → `"post"`.
- [ ] **Step 4: Run tests.** Expected: 8 passed.
- [ ] **Step 5: Smoke test.** Run `python3 tools/drill_stats.py`. Expected: all 9 categories `not ready`, no traceback.
- [ ] **Step 6: Commit.** `git add tools && git commit -m "feat(tools): add drill_stats for weekly training review"`

### Task 3: Kit and offline check

**Files:**
- Create: `training/women-tct-2026/kit.md`, `tools/check_kit.sh`

**Interfaces:**
- Produces: `tools/check_kit.sh` exits 0 when every required tool is present and 1 otherwise. It prints one line per tool: `ok <tool>` or `MISSING <tool> (<category>)`.

- [ ] **Step 1: Write `kit.md`.**
  - Per category, the tools with one verify command each. Builder picks; minimum: `web` (curl, Burp or ZAP, ffuf); `forensics` (file, exiftool, binwalk, foremost, volatility3); `re-pwn` (gdb + pwndbg or gef, ghidra, checksec, pwntools); `network` (wireshark, tshark); `mobile` (jadx, apktool); `programming` (python venv + pwntools); `crypto` (pycryptodome, sage or sympy); `misc` (cyberchef offline html, steghide, zsteg); `ai-iot` (binwalk, strings).
  - An **Offline** section: venv path, wordlists (rockyou, SecLists subset), local CyberChef, saved cheat sheets.
  - A **Competition-day routine** section, copied from the spec's Q-track bullets.
  - A **Before a commit in an event folder** line pointing to the LEARNINGS.md fake-secrets entry.
- [ ] **Step 2: Write `tools/check_kit.sh`.** It's a list of `tool:category` pairs that uses `command -v` for binaries and `python3 -c "import X"` (using the kit venv if it exists) for Python modules.
- [ ] **Step 3: Run** `sh tools/check_kit.sh; echo "exit=$?"`. Expected: it runs to the end, lists the current machine's state, and exits 1 if anything is missing. **Show the MISSING list to the user and ask before installing anything.**
- [ ] **Step 4: Commit.** `git add training tools/check_kit.sh && git commit -m "feat(training): add offline kit list and checker"`

### Task 4: Trim the re-solve backlog

**Files:**
- Modify: `practice/cylabacademy/queue.md` (the `## Re-solve` table)

- [ ] **Step 1: Keep 8 rows and set new due dates as F-track drills.** Crypto: Bigram Times, Crypto Civilization, EVEN RSA, Mini RSA → due 2026-11-19. Low Level Binary: ASCII Numbers, Picker I, Bit-O-Asm-1, Bit-O-Asm-2 → due 2026-11-26.
- [ ] **Step 2: Mark the other 9 rows** with `Result` = `Dropped 2026-11-15 — out of sprint scope (Women TCT 2026)`. Keep them in the table rather than deleting them; the history stays.
- [ ] **Step 3: Add one line under the `## Re-solve` intro:** "During the Women TCT 2026 sprint, a re-solve is logged as an F-track drill in `training/women-tct-2026/drill-log.md`. New re-solves come only from F-track drills at hint ≥ 2."
- [ ] **Step 4: Verify.** `grep -c 'Dropped 2026-11-15' practice/cylabacademy/queue.md` → 9.
- [ ] **Step 5: Commit.** `git commit -am "docs(queue): trim re-solve backlog to sprint scope"`

### Task 5: Notes: three new categories plus playbook slots

**Files:**
- Create: `notes/network.md`, `notes/mobile.md`, `notes/programming.md`
- Modify: the top of `notes/web.md`, `forensics.md`, `pwn.md`, `crypto.md`, `general.md`, `ai-ml.md`

- [ ] **Step 1: Create the three notes.** Each has a title and a `## Triage playbook (easy, ≤1 page)` section. Under it: 5–8 first-look commands taken from `kit.md` for that category, and the line `Fill from drills — each line must cite the drill that taught it.` No invented techniques.
- [ ] **Step 2: Insert the same `## Triage playbook (easy, ≤1 page)` section** right after the H1 of each existing note. Seed it only with checklist lines **already in that note** (moved up, not rewritten).
- [ ] **Step 3: Verify.** `grep -l 'Triage playbook' notes/*.md | wc -l` → 9. `osint.md` is out of scope, since OSINT isn't an event category.
- [ ] **Step 4: Commit.** `git add notes && git commit -m "docs(notes): add triage playbook slots for the 9 event categories"`

### Task 6: Sprint rules for Claude, plus links

**Files:**
- Create: `CLAUDE.md`
- Modify: `README.md` (one line under Learning Path), `LEARNING_PATH.md` (one line at the top)

- [ ] **Step 1: Write `CLAUDE.md`** (short) with a `## Women TCT 2026 sprint (until 2026-12-26)` section:
  - At session start, run `python3 tools/drill_stats.py`. If the current week's hours are well behind plan, or over 20 h, say so in one line.
  - From 2026-11-29, ask "registered yet?" every session until the README ☐ is ticked. The deadline is 2026-12-10.
  - Track rules: on Q-track drills, act as the competition AI (pair; agents only for grindy sub-tasks, local files only until the organizer confirms). On F-track drills, use `/ctf-hint` escalation only: no flags, no solving, and log the hint level.
  - Sunday review: fill `weekly/<YYYY>-W<nn>.md` from TEMPLATE with the user.
  - Never write the user's Solve Log or Prediction.
- [ ] **Step 2: Link the training folder** from `README.md` and `LEARNING_PATH.md`, one line each.
- [ ] **Step 3: Verify.** Run `python3 -m unittest tools/test_drill_stats.py` → pass. Run `grep -n 'training/women-tct-2026' README.md LEARNING_PATH.md` → 2 hits.
- [ ] **Step 4: Commit.** `git add CLAUDE.md README.md LEARNING_PATH.md && git commit -m "docs: add sprint rules for Claude and link training folder"`

---

## Out of this plan (done during the sprint, not the build)

Filling the playbooks, picking specific drill challenges, installing missing tools (needs the user's OK), reading the rules page (W1), and the mocks themselves.
