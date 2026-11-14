import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from drill_stats import CATEGORIES, Drill, easy_ready, hours_by_week, parse_log, week_of

HEADER = (
    "| date | challenge | category | source | track | box | taken | solved | ai | hint | note |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def log(*rows: str) -> str:
    return "# Drill Log\n\nlegend text\n\n" + HEADER + "".join(r + "\n" for r in rows)


class ParseTests(unittest.TestCase):
    def test_parses_valid_row(self):
        drills, problems = parse_log(
            log("| 2026-11-16 | [x](p/x) | network | pico | F | 30 | 25 | yes | no | 0 | ok |")
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            drills,
            [Drill(date(2026, 11, 16), "[x](p/x)", "network", "F", 30, 25, True, False, 0)],
        )

    def test_tolerates_messy_rows(self):
        text = log(
            "| 2026-11-16 | x | web | pico | Q | 30 | 25m | Yes |  no | 0 | |",
            "| 2026-11-17 | y | web | pico |",
        )
        drills, problems = parse_log(text)
        self.assertEqual(len(drills), 1)
        self.assertEqual(drills[0].taken, 25)
        self.assertTrue(drills[0].solved)
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("line 8:"), problems[0])

    def test_unknown_category_reported(self):
        drills, problems = parse_log(
            log("| 2026-11-16 | x | forensic | pico | F | 30 | 20 | yes | no | 0 | |")
        )
        self.assertEqual(drills, [])
        self.assertEqual(len(problems), 1)
        self.assertIn("forensic", problems[0])

    def test_empty_log(self):
        drills, problems = parse_log(log())
        self.assertEqual((drills, problems), ([], []))
        ready = easy_ready(drills)
        self.assertEqual(set(ready), set(CATEGORIES))
        self.assertFalse(any(ready.values()))


class WeekTests(unittest.TestCase):
    def test_week_of_boundaries(self):
        cases = {
            date(2026, 11, 14): "pre",
            date(2026, 11, 15): "W1",
            date(2026, 11, 21): "W1",
            date(2026, 11, 22): "W2",
            date(2026, 12, 12): "W4",
            date(2026, 12, 13): "W5",
            date(2026, 12, 25): "W6",
            date(2026, 12, 26): "post",
        }
        for d, want in cases.items():
            self.assertEqual(week_of(d), want, d)

    def test_hours_by_week(self):
        drills, _ = parse_log(
            log(
                "| 2026-11-16 | a | web | p | F | 60 | 60 | yes | no | 0 | |",
                "| 2026-11-18 | b | web | p | F | 30 | 30 | no | no | 0 | |",
                "| 2026-11-23 | c | web | p | F | 60 | 90 | no | no | 0 | |",
            )
        )
        self.assertEqual(hours_by_week(drills), {"W1": 1.5, "W2": 1.5})


class EasyReadyTests(unittest.TestCase):
    def ready(self, row: str) -> bool:
        drills, problems = parse_log(log(row))
        self.assertEqual(problems, [])
        return easy_ready(drills)["crypto"]

    def test_clean_easy_solve_is_ready(self):
        self.assertTrue(self.ready("| 2026-11-16 | x | crypto | p | F | 30 | 20 | yes | no | 0 | |"))

    def test_easy_ready_requires_unassisted(self):
        self.assertFalse(self.ready("| 2026-11-16 | x | crypto | p | Q | 30 | 20 | yes | yes | 0 | |"))
        self.assertFalse(self.ready("| 2026-11-16 | x | crypto | p | F | 30 | 20 | yes | no | 1 | |"))

    def test_easy_ready_requires_within_box(self):
        self.assertFalse(self.ready("| 2026-11-16 | x | crypto | p | F | 30 | 45 | yes | no | 0 | |"))

    def test_medium_box_does_not_count(self):
        self.assertFalse(self.ready("| 2026-11-16 | x | crypto | p | F | 60 | 20 | yes | no | 0 | |"))


class RobustnessTests(unittest.TestCase):
    def test_blank_line_inside_table_does_not_drop_rows(self):
        text = log(
            "| 2026-11-16 | a | web | p | F | 30 | 20 | yes | no | 0 | |",
            "",
            "| 2026-11-17 | b | crypto | p | F | 30 | 20 | yes | no | 0 | |",
        )
        drills, problems = parse_log(text)
        self.assertEqual([d.challenge for d in drills], ["a", "b"])
        self.assertEqual(problems, [])

    def test_row_missing_leading_pipe_is_reported(self):
        text = log(
            "2026-11-16 | a | web | p | F | 30 | 20 | yes | no | 0 | |",
            "| 2026-11-17 | b | crypto | p | F | 30 | 20 | yes | no | 0 | |",
        )
        drills, problems = parse_log(text)
        self.assertEqual([d.challenge for d in drills], ["b"])
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("line 7: not a table row"), problems[0])

    def test_default_log_path_is_repo_relative(self):
        import drill_stats
        self.assertTrue(drill_stats.DEFAULT_LOG.is_absolute())
        self.assertTrue(drill_stats.DEFAULT_LOG.exists())


if __name__ == "__main__":
    unittest.main()
