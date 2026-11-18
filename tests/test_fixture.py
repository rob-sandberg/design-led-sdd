"""The Tidepool Keeper checkpoints give the results the worked example describes."""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "plugins/dl-prototype/scripts"
CP = REPO / "examples/tidepool-keeper/checkpoints"
F = "specs/features/F001-daily-tide-gift"
sys.path.insert(0, str(SCRIPTS))
import spec_diff  # noqa: E402
import specdoc  # noqa: E402

# checkpoint: (approve, ticket, story S1); 0 pass, 1 fail, None no tasks yet
EXPECTED = {
    "02-draft": (1, 1, None),
    "03-clarified": (1, 1, None),
    "04-analysed": (1, 1, None),
    "05-reviewed": (0, 1, None),
    "06-approved": (0, 0, None),
    "07-ticketed": (0, 0, 0),
    "08-proved": (0, 0, 0),
    "09-tuned": (0, 0, 0),
    "10-revised": (1, 1, 1),
}


def check(cp, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "ready_check.py"), F, "--root", ".", *args],
                          cwd=CP / cp, capture_output=True, text=True).returncode


class FixtureTests(unittest.TestCase):
    def test_every_checkpoint_has_a_specs_folder(self):
        for cp in ["01-start", *EXPECTED]:
            self.assertTrue((CP / cp / "specs/constitution.md").exists(), cp)

    def test_ready_check_results(self):
        for cp, (approve, ticket, story) in EXPECTED.items():
            with self.subTest(cp=cp):
                self.assertEqual(check(cp, "--stage", "approve"), approve)
                self.assertEqual(check(cp, "--stage", "ticket"), ticket)
                if story is not None:
                    self.assertEqual(check(cp, "--stage", "story", "--story", "S1"), story)

    def test_tuning_then_rule_change(self):
        s8, s9, s10 = (specdoc.read(CP / c / F / "spec.md") for c in ("08-proved", "09-tuned", "10-revised"))
        tuned = spec_diff.compare(s8, s9)
        self.assertEqual((tuned["kind"], tuned["parameters"]), ("tuning", ["reset_time"]))
        revised = spec_diff.compare(s9, s10)
        self.assertEqual((revised["kind"], revised["rules"]["changed"]), ("rule", ["F001.claim-once"]))
        plan = specdoc.read(CP / "09-tuned" / F / "test-plan.md")
        self.assertEqual(sorted(c["case"] for c in spec_diff.affected_cases(plan, revised)),
                         ["TC-F001.claim-once-01", "TC-F001.claim-once-02", "TC-F001.claim-once-03"])


if __name__ == "__main__":
    unittest.main()
