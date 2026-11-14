"""Turn the training drill log into the numbers the Sunday review needs.

Usage: python3 tools/drill_stats.py [path-to-drill-log.md]
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

CATEGORIES: tuple[str, ...] = (
    "web", "forensics", "re-pwn", "network", "mobile",
    "programming", "crypto", "misc", "ai-iot",
)
DEFAULT_LOG = Path("training/women-tct-2026/drill-log.md")
COLUMNS = 11
EASY_BOX = 30
OVER_HOURS = 20

# Sprint weeks (inclusive start dates); before W1 = "pre", after W6 = "post".
WEEKS: tuple[tuple[str, date], ...] = (
    ("W1", date(2026, 11, 15)),
    ("W2", date(2026, 11, 22)),
    ("W3", date(2026, 11, 29)),
    ("W4", date(2026, 12, 6)),
    ("W5", date(2026, 12, 13)),
    ("W6", date(2026, 12, 20)),
)
SPRINT_END = date(2026, 12, 25)


@dataclass
class Drill:
    date: date
    challenge: str
    category: str
    track: str
    box: int
    taken: int
    solved: bool
    ai: bool
    hint: int


def _yes_no(cell: str) -> bool:
    if cell not in ("yes", "no"):
        raise ValueError(f"expected yes/no, got {cell!r}")
    return cell == "yes"


def _minutes(cell: str) -> int:
    return int(cell.removesuffix("m").strip())


def _parse_row(cells: list[str]) -> Drill:
    norm = [c.strip().lower() for c in cells]
    category = norm[2]
    if category not in CATEGORIES:
        raise ValueError(f"unknown category {category!r}")
    track = norm[4].upper()
    if track not in ("Q", "F"):
        raise ValueError(f"track must be Q or F, got {cells[4].strip()!r}")
    hint = int(norm[9] or "0")
    if not 0 <= hint <= 3:
        raise ValueError(f"hint must be 0-3, got {hint}")
    return Drill(
        date=date.fromisoformat(norm[0]),
        challenge=cells[1].strip(),
        category=category,
        track=track,
        box=_minutes(norm[5]),
        taken=_minutes(norm[6]),
        solved=_yes_no(norm[7]),
        ai=_yes_no(norm[8]),
        hint=hint,
    )


def parse_log(text: str) -> tuple[list[Drill], list[str]]:
    drills: list[Drill] = []
    problems: list[str] = []
    in_table = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = stripped.strip("|").split("|")
        first = cells[0].strip().lower()
        if first == "date":
            in_table = True
            continue
        if not in_table or set(stripped) <= set("|-: "):
            continue
        if len(cells) != COLUMNS:
            problems.append(f"line {lineno}: expected {COLUMNS} columns, got {len(cells)}")
            continue
        try:
            drills.append(_parse_row(cells))
        except ValueError as exc:
            problems.append(f"line {lineno}: {exc}")
    return drills, problems


def week_of(d: date) -> str:
    if d < WEEKS[0][1]:
        return "pre"
    if d > SPRINT_END:
        return "post"
    label = WEEKS[0][0]
    for name, start in WEEKS:
        if d >= start:
            label = name
    return label


def hours_by_week(drills: list[Drill]) -> dict[str, float]:
    minutes: dict[str, int] = {}
    for d in drills:
        wk = week_of(d.date)
        minutes[wk] = minutes.get(wk, 0) + d.taken
    return {wk: m / 60 for wk, m in minutes.items()}


def easy_ready(drills: list[Drill]) -> dict[str, bool]:
    ready = {c: False for c in CATEGORIES}
    for d in drills:
        if d.box <= EASY_BOX and d.solved and not d.ai and d.hint == 0 and d.taken <= d.box:
            ready[d.category] = True
    return ready


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_LOG
    drills, problems = parse_log(path.read_text(encoding="utf-8"))

    print(f"Drills: {len(drills)}\n\nHours by week:")
    hours = hours_by_week(drills)
    if not hours:
        print("  (none)")
    for wk in sorted(hours):
        flag = f"  OVER {OVER_HOURS}h" if hours[wk] > OVER_HOURS else ""
        print(f"  {wk}: {hours[wk]:.1f} h{flag}")

    print("\nEasy-ready (solved within a ≤30 min box, no AI, no hint):")
    for cat, ok in easy_ready(drills).items():
        print(f"  {cat:<12} {'ready' if ok else 'not ready'}")

    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
