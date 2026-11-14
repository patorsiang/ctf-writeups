# Women Thailand Cyber Top Talent 2026 — Training

Target: **win the WOpen tier** of Women Thailand Cyber Top Talent 2026
(NCSA + Huawei, https://ctf.in.th/challenge/4937/). There are two stages: reach
the final (top 10 WOpen teams in the qualifier), then place top 3 in the final.

Design: [docs/superpowers/specs/2026-11-14-women-tct-2026-training-design.md](../../docs/superpowers/specs/2026-11-14-women-tct-2026-training-design.md)

- [ ] **Registered** (by 2026-12-01; the deadline is 2026-12-10)

## The event

| | Qualifier | Final |
|---|---|---|
| Date | Sat 2026-12-12, 09:00–16:00 (7 h) | Sat 2026-12-26, 09:00–15:00 (6 h) |
| Where | Online | On-site at NCSA |
| AI | **Allowed** | **Not allowed** |

Solo (teams of up to 3 are allowed). 9 categories: `web`, `forensics`, `re-pwn`,
`network`, `mobile`, `programming`, `crypto`, `misc`, `ai-iot`.

## Goals

1. [ ] **Easy-ready in all 9 categories** by 2026-11-28
2. [ ] **Medium-ready in forensics, crypto, misc** by 2026-12-05
3. [ ] **Q-track:** the kit plus an AI-assisted workflow, rehearsed in the 7 h mock before 2026-12-12
4. [ ] **F-track:** unassisted solving, rehearsed in the 6 h no-AI mock before 2026-12-26
5. [ ] Every drill measured in [drill-log.md](drill-log.md)

## Schedule

| Week | Dates | Focus |
|---|---|---|
| W1 | 11-15 → 11-21 | Read the rules page (solo team OK? notes or internet in the final? agents?). Build the [kit](kit.md). Easy-ready: network, mobile. Crypto re-solves (due 11-19). |
| W2 | 11-22 → 11-28 | Easy-ready: web, programming, re-pwn, ai-iot. Binary re-solves (due 11-26). Checkpoint: every category in the easy-ready table is green or flagged. |
| W3 | 11-29 → 12-05 | **Register by 12-01.** Medium: forensics, crypto (CryptoHack AES), misc. **Sat 12-05: [qualifier mock](mocks/2026-12-05-qualifier-mock.md).** |
| W4 | 12-06 → 12-12 | Fix gaps from the mock only. Keep it light. Kit check 12-11. **12-12 qualifier.** |
| W5 | 12-13 → 12-19 | F-track heavy on weak spots from the qualifier. **Sat 12-19: [final mock](mocks/2026-12-19-final-mock.md).** |
| W6 | 12-20 → 12-25 | Fix gaps from the mock, then taper on 12-24/25. **12-26 final.** |

The weekly budget is 10–15 h. W2–W3 may go over. Anything over 20 h gets flagged at
the Sunday review.

## Easy-ready

Run `python3 tools/drill_stats.py` at each Sunday review and copy the result here.
A category is ready once it has at least one easy drill (box ≤ 30 min) solved
within the box, with **no AI and no hint**.

| Category | Ready? | As of |
|---|---|---|
| web | | |
| forensics | | |
| re-pwn | | |
| network | | |
| mobile | | |
| programming | | |
| crypto | | |
| misc | | |
| ai-iot | | |

## Files

- [drill-log.md](drill-log.md): one row per drill
- [kit.md](kit.md): tools, offline setup, competition-day routine
- [mocks/](mocks): the two full-length rehearsals
- [weekly/](weekly): Sunday reviews (copy [TEMPLATE.md](weekly/TEMPLATE.md))
