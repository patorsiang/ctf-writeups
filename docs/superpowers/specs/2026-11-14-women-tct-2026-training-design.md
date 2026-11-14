# Women Thailand Cyber Top Talent 2026 — Training System Design

Date: 2026-11-14 · Status: draft, awaiting approval

## Intent

Turn this repo from a writeup archive into a training system with one target:
**win the WOpen tier of Women Thailand Cyber Top Talent 2026** (NCSA + Huawei,
https://ctf.in.th/challenge/4937/). First real competition aimed at a result,
not just participation.

"Win" is staged: (1) reach the final = top 10 WOpen teams nationwide in the
qualifier; (2) place top 3 in the final.

## The event (facts from the event page)

| | Qualifier | Final |
|---|---|---|
| Date | Sat 2026-12-12, 09:00–16:00 (7 h) | Sat 2026-12-26, 09:00–15:00 (6 h) |
| Where | Online | On-site at NCSA |
| AI | **Allowed** | **Not allowed** |

- Registration: 2026-11-10 → **2026-12-10**. Teams ≤ 3, one team per person.
- Tier: **WOpen** (general public / staff, Thai nationality). 10 WOpen teams reach the final.
- Format: Jeopardy, points scale with difficulty.
- 9 categories: Web, Digital Forensic, RE & Pwn, Network Security, Mobile
  Security, Programming, Cryptography, Misc, Other (AI & IoT).

## Constraints

- **Solo** (worst case). If teammates join, they take whole categories; the plan
  otherwise stands.
- **4 weeks** to the qualifier, then 2 weeks to the final.
- **Time budget: ~10–15 h/week** (my call — foundation.md logs real weeks at
  10–20 h against a stated 20+; plan to the low end so the plan survives a bad week).
- Existing repo conventions stay: Prediction + Solve Log + 7-day re-solve
  (CONTRIBUTING.md Learning Rules), LEARNINGS.md append-only, topic notes in `notes/`.
- Current state: strong-ish in Forensics/Misc/Crypto (classical + basic RSA) and AI;
  thin Web; near-empty Pwn/Rev (`notes/pwn.md` 393 B); **nothing** on Network or
  Mobile. 17 re-solves overdue (since 2026-10-08), none done. No commits since
  Hackloween (2026-10-31).
- Hackloween lessons already logged: probing without recording dead ends,
  README lag during a match, fake secrets blocking pushes.

## Goals

1. **Easy-ready in all 9 categories** by 2026-11-28: for each, can solve a typical
   easy challenge from this organizer within ~30 min, with a one-page playbook.
2. **Medium-ready in Forensics, Crypto, Misc** (strongest three) by 2026-12-05.
3. **Q-track:** a competition kit and an AI-assisted workflow rehearsed in a full
   7-hour mock before 2026-12-12.
4. **F-track:** unassisted solving rehearsed in a full 6-hour no-AI mock before
   2026-12-26.
5. Every drill measured (time, solved, AI used) so weekly re-plans use data, not mood.

## Non-goals

- Deep pwn (heap, ROP chains beyond ret2win). Hard RE & Pwn points are conceded.
- Polished public writeups during the sprint. Drill READMEs are short; polishing
  happens after 2026-12-26.
- Finishing CyLab learning paths for their own sake.
- New tooling projects (no building a CTF platform, no automation beyond small scripts).

## Anti-goals (fail even if "done")

- A beautiful plan file and no drill log entries. **Success is measured by
  drills logged, not structure created.**
- Training only with AI and walking into the no-AI final unable to solve alone.
- Registration missed (deadline 2026-12-10). The user chose to register in
  December. Hard date: **2026-12-01**, which leaves 9 days to fix problems.
  Claude raises it at every session from 2026-11-29 until it's done.
- Burnout before 12-12. Goals win over the time cap (user decision): W2–W3 may
  run over 15 h; W4 is deliberately light to recover. If a W2/W3 week passes ~20 h
  (the top of what foundation.md has actually logged), the Sunday review flags it.

## Approaches considered

- **A. Easy everywhere + depth in strongest 3, two tracks (chosen by user).**
  Easy challenges are the cheapest points on a jeopardy board; solo, breadth of
  easy beats depth in a few. Two tracks because the rounds test different skills.
  Trade-off: concede hard pwn.
- **B. Even breadth across 9.** Simple, but shallow everywhere; top 10 needs some mediums.
- **C. Specialize 4–5, skip rest.** Deepest, but throws away the cheapest points
  (easy Network/Mobile).

## Design

### Repo layout (new)

```text
training/women-tct-2026/
  README.md        # the plan: dates, weekly blocks, goals, status checkboxes
  drill-log.md     # one row per drill (table below)
  kit.md           # competition-day kit: tools installed + verified, env, checklist
  mocks/
    2026-12-05-qualifier-mock.md   # 7 h, AI allowed
    2026-12-19-final-mock.md       # 6 h, no AI
  weekly/
    2026-W47.md …  # Sunday review: what the log says, re-plan next week
notes/
  network.md       # new
  mobile.md        # new
  programming.md   # new
  <existing>.md    # each gets a "## Triage playbook (easy, ≤1 page)" section at top
```

Drill challenges themselves live where the repo already puts them
(`practice/<platform>/…`, `events/<year>/<event>/…`). The training folder only
indexes and measures.

### Drill log row

`| date | challenge (link) | category | source | track Q/F | time-box | time taken | solved? | AI? | hint level | note |`

A drill is time-boxed (easy 30 min, medium 60 min). Over the box = log it as
unsolved, write the dead ends (Hackloween lesson), move on. Real competitions
reward abandoning.

### Schedule

| Week | Dates | Focus |
|---|---|---|
| W1 | 11-15 → 11-21 | Read the rules page (solo team OK? notes/internet in final? agents?). Build `kit.md` (install + verify tools per category). Easy-ready: Network (pcap/Wireshark/tshark), Mobile (APK: jadx, apktool, strings/secrets). Re-solve triage. |
| W2 | 11-22 → 11-28 | Easy-ready: Web (PortSwigger Apprentice core: SQLi, XSS, auth, access control, path traversal), Programming (nc + pwntools scripting), RE (Ghidra basics, ret2win-level pwn), IoT/AI (firmware strings/binwalk, prompt injection). Checkpoint: easy-ready table all green or flagged. |
| W3 | 11-29 → 12-05 | **Register by 12-01.** Medium: Forensics, Crypto (CryptoHack Symmetric/AES), Misc. **Sat 12-05: 7 h qualifier mock** (AI allowed). |
| W4 | 12-06 → 12-11 | Fix mock gaps only. Light. Final kit check 12-11. **12-12 qualifier.** |
| W5–6 | 12-13 → 12-25 | F-track heavy: no-AI timed drills on weak spots from qualifier. **Sat 12-19: 6 h no-AI final mock.** Taper 12-24/25. **12-26 final.** |

Each week: ~70% Q/F drills, ~20% playbook writing (from what the drills taught),
~10% Sunday review. F-track (no AI) runs every week from W1, minimum 2 drills/week,
rising to most drills in W5–6.

### Two tracks

- **Q-track (qualifier, AI allowed).** The skill is *throughput*: triage the
  board, pick by points/minute, use AI as a pair (paste source, ask for vuln
  class, generate solver), verify, submit, move on. `kit.md` includes a
  competition-day routine: first 15 min scan whole board and rank; time-box per
  challenge; README stub the moment a challenge is solved or dropped.
- **Who solves in the qualifier (user decision: "a or c").** Default: **the user
  drives** (triage, analysis, submit); Claude pairs (explain code, name the vuln
  class, write solvers). **Agents are allowed only for grindy sub-tasks**: brute
  force, scripted interaction, bulk decoding. The user chooses each time, and the
  drill log records it. The 12-05 mock rehearses this mix. Before any agent touches
  a qualifier server, confirm with the organizer that "AI allowed" covers it.
  Until then, agents only work on local files.
- **F-track (final, no AI).** The skill is *recall*: playbooks must live in your
  head or on paper. Drills done with AI off, Claude only via `/ctf-hint` escalation
  if stuck past the box (logged as hint level).

### Practice sources (priority order)

1. ctf.in.th past events + its write-ups section + the Thailand Cyber Top Talent 2026
   final replay — same organizer, same style. Playability of old challenges to be
   verified in W1.
2. picoGym (easy breadth, all categories incl. some network/forensics).
3. PortSwigger Web Security Academy (Web), CryptoHack (Crypto/AES).
4. pwn.college (RE/pwn basics only, time-boxed — non-goal to go deep).
5. CyLab Academy paths — only where they map to a gap.

### Re-solve backlog

17 overdue is not realistic on top of this. **My call:** keep re-solves only for
challenges in target categories that teach a technique likely to appear
(the 4 crypto + Low Level Binary ones); mark the rest `Dropped — out of sprint scope`
in `queue.md` with today's date. Kept re-solves count as F-track drills.

### Drill cost and new re-solves (my call)

- Every drill gets a short README: `Prediction` (one line, before starting) +
  `Solve Log` (own words, during) + result. No polished walkthrough during the sprint.
- **Q-track drills never create re-solves.** AI use is the point of the track.
- **F-track drills create a re-solve only when hint level ≥ 2** (a technique was
  given, not just a nudge). That keeps the re-solve queue proportional to real gaps.

### Offline-capable kit (my call)

`kit.md` assumes **the final may have no internet** until the rules say otherwise:
local copies of key docs/cheat sheets, wordlists (rockyou, SecLists subset),
pinned Python venv with pwntools/pycryptodome/etc., tools installed natively
(not via a web service). Cheap insurance, and it removes the dependency on a
late rules answer.

### How Claude behaves during the sprint

- Q-track drills: Claude may be used as the competition-day AI would be — and
  that usage is logged (`AI? yes`).
- F-track drills: mentor only via `/ctf-hint`, no flags, no solving.
- Claude checks `drill-log.md` at session start and calls out a week falling
  behind plan.
- Sunday review: Claude reads the log, writes the weekly review with the user,
  re-plans the next week's categories by measured gap.

## Decided by the user

- Target: Women Thailand Cyber Top Talent 2026, **WOpen**, aim to win.
- **Solo** as planning baseline.
- Approach **A**.
- Qualifier: user drives, AI pairs; agents only for grindy sub-tasks.
- Goals win over the time cap; W2–W3 may run over 15 h.

## My calls (correct if wrong)

- 10–15 h/week baseline budget (W2–W3 may exceed).
- Q-track drills don't create re-solves; F-track ones do at hint level ≥ 2.
- Kit is offline-capable from the start.
- Weekly schedule and dates above, mock dates 12-05 and 12-19.
- Re-solve trimming rule.
- Medium focus = Forensics, Crypto, Misc.
- Layout under `training/women-tct-2026/`.

## Left to the builder

- Exact contents of each playbook and `kit.md` tool list.
- Which specific past challenges fill each drill slot (pick from sources in order).
- Template text for weekly review and mock files.

## Open (verify, not decide)

- Whether past ctf.in.th challenges are still playable.
- Whether paper notes / offline docs are allowed in the on-site final (changes
  whether playbooks are memorized or printed). Ask organizer / check rules page in W1.
- Whether personal laptop and internet access are allowed in the final.
- Whether "AI allowed" in the qualifier covers agents interacting with challenge servers.
