"""Run with:  python3 -m unittest discover tests"""
import datetime as dt
import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class CritterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)
        os.environ.update({"CRITTER_USER": "octocat", "GITHUB_REPOSITORY": "octocat/octocat",
                           "CRITTER_SPECIES": "crab", "CRITTER_NAME": ""})
        Path("README.md").write_text("# Hi, I'm Octocat\n\nI build things.\n")

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def run_day(self, day, food):
        os.environ["CRITTER_TODAY"] = day
        import critter
        critter = importlib.reload(critter)
        critter.real_activity = (lambda: food) if not isinstance(food, Exception) else self._raise(food)
        msgs = []
        for cmd in (critter.feed, critter.diary, critter.trophy):
            cmd()
            msgs.append(Path(".critter-msg").read_text().strip())
        return critter, msgs

    @staticmethod
    def _raise(exc):
        def f():
            raise exc
        return f

    def days(self, n):
        start = dt.date(2026, 1, 1)
        return [(start + dt.timedelta(i)).isoformat() for i in range(n)]

    def test_first_day_keeps_existing_readme_and_appends_block(self):
        self.run_day("2026-01-01", 3)
        text = Path("README.md").read_text()
        self.assertTrue(text.startswith("# Hi, I'm Octocat\n\nI build things."))
        self.assertIn("Clawdia the crab, feeling", text)
        self.assertEqual(text.count("COMMIT-CRITTER:START"), 1)

    def test_block_is_replaced_in_place_not_duplicated(self):
        Path("README.md").write_text("top\n<!-- COMMIT-CRITTER:START -->\nold\n<!-- COMMIT-CRITTER:END -->\nbottom\n")
        self.run_day("2026-01-01", 1)
        text = Path("README.md").read_text()
        self.assertTrue(text.startswith("top\n") and text.endswith("bottom\n"))
        self.assertNotIn("old", text)

    def test_two_commits_normally_three_on_milestone(self):
        for i, day in enumerate(self.days(7)):
            _, msgs = self.run_day(day, 2)
            expected = 3 if i == 6 else 2
            self.assertEqual(sum(bool(m) for m in msgs), expected, (day, msgs))
        self.assertIn("one week", msgs[2])
        trophies = Path(".critter/trophies.md").read_text()
        self.assertNotIn("No trophies yet", trophies)
        self.assertEqual(trophies.count("🏆"), 1)

    def test_dark_theme(self):
        os.environ["CRITTER_THEME"] = "dark"
        try:
            c, _ = self.run_day("2026-01-01", 1)
        finally:
            del os.environ["CRITTER_THEME"]
        self.assertIn(c.sprites.PANEL["dark"]["F"], Path(".critter/critter.svg").read_text())

    def test_unknown_theme_falls_back_to_light(self):
        os.environ["CRITTER_THEME"] = "neon"
        try:
            c, _ = self.run_day("2026-01-01", 1)
        finally:
            del os.environ["CRITTER_THEME"]
        self.assertIn(c.sprites.PANEL["light"]["F"], Path(".critter/critter.svg").read_text())

    def test_history_keeps_the_last_seven_days(self):
        for i, day in enumerate(self.days(9)):
            c, _ = self.run_day(day, i)
        self.assertEqual(c.load()["history"], [2, 3, 4, 5, 6, 7, 8])

    def test_sizes(self):
        import xml.etree.ElementTree as ET
        import sprites
        for size, width in (("small", "264"), ("medium", "576"), ("full", "100%")):
            os.environ["CRITTER_SIZE"] = size
            try:
                Path(".critter/state.json").unlink(missing_ok=True)
                self.run_day("2026-01-01", 3)
            finally:
                del os.environ["CRITTER_SIZE"]
            self.assertIn(f'width="{width}"', Path("README.md").read_text(), size)
            card = ET.fromstring(Path(".critter/critter.svg").read_text())
            w, h = sprites.SIZES[size]
            self.assertEqual(card.get("viewBox"), f"0 0 {w} {h}", size)

    def test_unknown_size_falls_back_to_medium(self):
        os.environ["CRITTER_SIZE"] = "huge"
        try:
            self.run_day("2026-01-01", 1)
        finally:
            del os.environ["CRITTER_SIZE"]
        self.assertIn('width="576"', Path("README.md").read_text())

    def test_trophies_page_exists_from_day_one(self):
        self.run_day("2026-01-01", 1)
        self.assertIn("No trophies yet", Path(".critter/trophies.md").read_text())

    def test_rerun_same_day_is_noop(self):
        self.run_day("2026-01-01", 2)
        _, msgs = self.run_day("2026-01-01", 2)
        self.assertEqual(msgs, ["", "", ""])

    def test_no_activity_makes_it_hungry_and_resets_streak(self):
        for day in self.days(3):
            self.run_day(day, 0)
        c, _ = self.run_day("2026-01-04", 0)
        s = c.load()
        self.assertEqual(s["real_streak"], 0)
        self.assertIn(c.mood(s), ("hungry", "starving"))

    def test_api_failure_still_commits(self):
        c, msgs = self.run_day("2026-01-01", RuntimeError("boom"))
        self.assertIn("API hiccup", msgs[0])
        self.assertTrue(msgs[1])

    def test_unknown_species_falls_back_to_snail(self):
        os.environ["CRITTER_SPECIES"] = "dragon"
        c, _ = self.run_day("2026-01-01", 1)
        self.assertIn("the snail", Path("README.md").read_text())

    def test_every_species_has_every_mood(self):
        import critter
        import xml.etree.ElementTree as ET
        self.assertEqual(set(critter.SPECIES), set(critter.sprites.SPECIES))
        for name, sp in critter.SPECIES.items():
            for m in critter.MOODS:
                self.assertTrue(sp["diary"][m], name)
                ET.fromstring(critter.sprites.svg(name, m, title="<Tom & Jerry>"))  # well-formed

    def test_sprite_is_drawn_and_linked(self):
        self.run_day("2026-01-01", 6)
        self.assertIn('<img src=".critter/critter.svg"', Path("README.md").read_text())
        card = Path(".critter/critter.svg").read_text()
        self.assertIn("<title>Clawdia the crab, feeling ecstatic. Fullness 10/10, ate 6 today", card)
        self.assertIn('transform="scale(.5)"', card)  # stats panel is drawn


if __name__ == "__main__":
    unittest.main()
