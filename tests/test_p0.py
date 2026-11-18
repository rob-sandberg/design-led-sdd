"""Regression tests for dl-prototype's two P0 behaviours: the Ready gate and the
open-questions register. They run the plugin's scripts on a disposable project and
need no model and no network.

Run from the repository root:  python3 -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "plugins" / "dl-prototype" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import pointer  # noqa: E402
import ready_check  # noqa: E402
import register  # noqa: E402
import spec_diff  # noqa: E402
import specdoc  # noqa: E402

CONSTITUTION = """# Constitution: Test Game

- Status: Agreed
- Owner: Designer
- Last updated: 2026-11-18

## The game in three lines

A test game.

{register}
## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-11-18 | First version | Designer |
"""

GLOSSARY = """# Glossary

| Term (player-facing) | Code term | Means | Used in |
| --- | --- | --- | --- |
| Reset | daily_reset | The moment a new gift can be claimed | F001 |
"""

REGISTER = """# Open questions

## Open

### F001: Daily gift

| ID | Question | Proposal | Owner | Blocking | Raised | Spec | Was |
| --- | --- | --- | --- | --- | --- | --- | --- |
{rows}

## Resolved

| ID | Question | Answer | Decided by | Date |
| --- | --- | --- | --- | --- |
| OQ-F001-001 | Reset time? | 04:00 local | Designer | 2026-11-18 |

## Deferred

| ID | Question | Why deferred | Revisit at |
| --- | --- | --- | --- |
"""

SPEC = """# F001: Daily gift

- Status: {status}
- Owner: Designer
- Last updated: 2026-11-18

## Intent

Give lapsed players a reason to open the game once a day.

## Player experience

Claiming is one tap and feels like a small surprise.

## Scope

- In: one gift per day.
- Out, for now: streaks.

## Rules

### F001.claim-once: The gift can be claimed once per day

```gherkin
When      the player opens the beach
Provided  the player has not claimed since the last Reset
Then      the gift can be claimed
Otherwise the beach shows the time to the next Reset
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| first open after the Reset | yes | gift shown | |
| claimed {minutes} minutes ago | no | countdown shown | |

## Parameters

| Name | Value | Unit | Notes |
| --- | --- | --- | --- |
| reset_time | {reset} | local time | |

## Terms

| Term | Means |
| --- | --- |
| Reset | When a new gift can be claimed |

## Approval

{approval}

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-11-18 | First draft | Designer |
"""

NO_APPROVAL = "- Ready: No\n- Approved by:\n- Date:\n- Revision:\n- Commit:\n- Analysis:"

REPORT = """# Analysis: F001 Daily gift (2026-11-18, run {nn})

- Spec revision: {rev}
- Spec commit: working copy
- Context: constitution {crev}, glossary {grev}
- Inputs: spec.md, constitution.md, glossary.md, open-questions.md
- Access: Read only, inputs passed by the lead

## Verdict

Findings to resolve: {nb} blocking, {na} advisory

## Findings

| # | Kind | Where | Finding | Evidence | Suggested fix | Severity |
| --- | --- | --- | --- | --- | --- | --- |
{findings}

## Resolutions

| # | Disposition | Reason | Decided by | Date |
| --- | --- | --- | --- | --- |
{resolutions}
"""

TASKS = """# F001: Daily gift, tasks

- Built from: spec revision {rev}, approved 2026-11-18

## Story S1: Claim the gift

**Status:** {status}

**Spec rules:** F001.claim-once

Uses `reset_time`.
"""


def quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        code = fn(*a, **k)
    return code, buf.getvalue()


class Project:
    """A disposable project in the method's layout."""

    def __init__(self, register_section="", rows="| OQ-F001-002 | Offline? | Grey the shell | Designer | No | 2026-11-18 | F001 | |"):
        self.root = Path(tempfile.mkdtemp(prefix="dlp-"))
        self.specs = self.root / "specs"
        self.feature = self.specs / "features" / "F001-daily-gift"
        self.feature.mkdir(parents=True)
        (self.specs / "constitution.md").write_text(CONSTITUTION.format(register=register_section))
        (self.specs / "glossary.md").write_text(GLOSSARY)
        self.write_register(rows)
        self.write_spec()

    def write_register(self, rows, path=None):
        (path or self.specs / "open-questions.md").write_text(REGISTER.format(rows=rows))

    def write_spec(self, status="Draft", approval=NO_APPROVAL, minutes="10", reset="04:00"):
        (self.feature / "spec.md").write_text(SPEC.format(status=status, approval=approval, minutes=minutes, reset=reset))

    @property
    def spec_text(self):
        return (self.feature / "spec.md").read_text()

    def rev(self):
        return specdoc.revision(self.spec_text)

    def write_report(self, nn="01", findings="| 1 | Wording | F001.claim-once | Unclear verb | Line 20 | Say claim | Advisory |",
                     resolutions="", nb=0, na=1, rev=None):
        crev = specdoc.revision((self.specs / "constitution.md").read_text())
        grev = specdoc.revision((self.specs / "glossary.md").read_text())
        name = f"analysis-2026-11-18-{nn}.md"
        (self.feature / name).write_text(REPORT.format(nn=nn, rev=rev or self.rev(), crev=crev, grev=grev, nb=nb, na=na,
                                                       findings=findings, resolutions=resolutions))
        return name

    def approve(self, report_name, by="Designer"):
        appr = (f"- Ready: Yes\n- Approved by: {by}\n- Date: 2026-11-18\n- Revision: {self.rev()}\n"
                f"- Commit: working copy\n- Analysis: {report_name}")
        self.write_spec(status="Ready", approval=appr)

    def check(self, stage="ticket", story=None, rows_file=None):
        g, _ = ready_check.run(self.feature, stage, story, self.root, rows_file)
        return g

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.p = Project()

    def tearDown(self):
        self.p.cleanup()

    def assertPass(self, g):
        self.assertEqual(g.fails, [], "expected the gate to pass")

    def assertFailWith(self, g, words):
        self.assertTrue(any(words in f for f in g.fails), f"expected a failure containing {words!r}, got {g.fails}")


class RevisionTests(Base):
    def test_status_approval_and_changelog_do_not_change_revision(self):
        before = self.p.rev()
        self.p.approve("analysis-2026-11-18-01.md")
        text = self.p.spec_text.replace("- Last updated: 2026-11-18", "- Last updated: 2026-12-01")
        text += "| 2026-12-01 | Ready | Designer |\n"
        self.assertEqual(specdoc.revision(text), before)

    def test_design_edit_changes_revision(self):
        before = self.p.rev()
        self.p.write_spec(minutes="11")
        self.assertNotEqual(self.p.rev(), before)

    def test_trailing_spaces_and_blank_runs_ignored(self):
        before = self.p.rev()
        text = self.p.spec_text.replace("## Intent\n", "## Intent   \n\n\n")
        self.assertEqual(specdoc.revision(text), before)


class ReadyGateTests(Base):
    def test_happy_path_approve_then_ticket(self):
        name = self.p.write_report()
        self.assertPass(self.p.check("approve"))
        self.p.approve(name)
        g = self.p.check("ticket")
        self.assertPass(g)
        self.assertTrue(any("advisory" in n for n in g.notes))

    def test_ready_label_without_approval_stops_tickets(self):
        self.p.write_report()
        self.p.write_spec(status="Ready")
        self.assertFailWith(self.p.check("ticket"), "status says Ready")

    def test_missing_report_stops_tickets(self):
        self.p.approve("analysis-2026-11-18-01.md")
        self.assertFailWith(self.p.check("ticket"), "no analysis report")

    def test_changed_revision_stops_tickets(self):
        name = self.p.write_report()
        self.p.approve(name)
        text = self.p.spec_text.replace("claimed 10 minutes ago", "claimed 12 minutes ago")
        (self.p.feature / "spec.md").write_text(text)
        g = self.p.check("ticket")
        self.assertFailWith(g, "approval has lapsed")
        self.assertFailWith(g, "rerun analyze")

    def test_open_blocking_question_stops_ready(self):
        self.p.write_register("| OQ-F001-002 | Offline? | Grey the shell | Designer | Yes | 2026-11-18 | F001 | |")
        name = self.p.write_report()
        self.p.approve(name)
        self.assertFailWith(self.p.check("ticket"), "open and blocking")

    def test_unknown_blocking_status_needs_triage(self):
        self.p.write_register("| OQ-F001-002 | Offline? | Grey the shell | Designer | ? | 2026-11-18 | F001 | |")
        self.p.write_report()
        self.assertFailWith(self.p.check("approve"), "triage")

    def test_unresolved_blocking_finding_stops_ready(self):
        self.p.write_report(findings="| 1 | Gap | F001.claim-once | No offline case | Line 18 | Add it | Blocking |", nb=1, na=0)
        self.assertFailWith(self.p.check("approve"), "unresolved")

    def test_dismissed_blocker_needs_reason_and_decision_maker(self):
        f = "| 1 | Gap | F001.claim-once | No offline case | Line 18 | Add it | Blocking |"
        self.p.write_report(findings=f, nb=1, na=0, resolutions="| 1 | Dismissed | | | 2026-11-18 |")
        self.assertFailWith(self.p.check("approve"), "without a reason")
        self.p.write_report(nn="02", findings=f, nb=1, na=0,
                            resolutions="| 1 | Dismissed | Offline is out of the slice | Designer | 2026-11-18 |")
        self.assertPass(self.p.check("approve"))

    def test_blocker_fixed_by_edit_needs_a_check_of_the_edited_revision(self):
        f = "| 1 | Gap | F001.claim-once | Wrong minute | Line 20 | Fix it | Blocking |"
        self.p.write_report(findings=f, nb=1, na=0)
        self.p.write_spec(minutes="15")  # the designer's fix
        g = self.p.check("approve")
        self.assertFailWith(g, "rerun analyze on the current revision")
        self.p.write_report(nn="02", findings="| 1 | Wording | Scope | Fine | - | - | Advisory |")
        self.assertPass(self.p.check("approve"))

    def test_glossary_change_after_report_needs_recheck(self):
        self.p.write_report()
        (self.p.specs / "glossary.md").write_text(GLOSSARY + "| Gift | gift | A reward | F001 |\n")
        self.assertFailWith(self.p.check("approve"), "glossary.md has changed")

    def test_term_missing_from_glossary(self):
        (self.p.specs / "glossary.md").write_text("# Glossary\n\n| Term | Means |\n| --- | --- |\n| Gift | A reward |\n")
        self.p.write_report()
        self.assertFailWith(self.p.check("approve"), "not in the glossary")

    def test_one_sided_examples_fail(self):
        (self.p.feature / "spec.md").write_text(self.p.spec_text.replace("| no | countdown shown", "| yes | countdown shown"))
        self.p.write_report()
        self.assertFailWith(self.p.check("approve"), "one side of the guard")

    def test_latest_report_wins_including_old_names(self):
        self.p.write_report(nn="01", findings="| 1 | Gap | X | Y | Z | W | Blocking |", nb=1, na=0)
        self.p.write_report(nn="02")
        self.assertPass(self.p.check("approve"))
        order = [p.name for p in specdoc.reports(self.p.feature)]
        (self.p.feature / "analysis-2026-11-17.md").write_text("old")
        (self.p.feature / "analysis-2026-11-17-pass2.md").write_text("old")
        order = [p.name for p in specdoc.reports(self.p.feature)]
        self.assertEqual(order[:2], ["analysis-2026-11-17.md", "analysis-2026-11-17-pass2.md"])
        self.assertEqual(order[-1], "analysis-2026-11-18-02.md")

    def test_cli_exit_codes(self):
        self.p.write_report()
        code, out = quiet(ready_check.main, [str(self.p.feature), "--stage", "approve", "--root", str(self.p.root)])
        self.assertEqual(code, 0, out)
        code, out = quiet(ready_check.main, [str(self.p.feature), "--stage", "ticket", "--root", str(self.p.root)])
        self.assertEqual(code, 1, out)


class StoryTests(Base):
    def test_story_ready_against_current_revision(self):
        name = self.p.write_report()
        self.p.approve(name)
        rev = self.p.rev()
        (self.p.feature / "tasks.md").write_text(TASKS.format(rev=rev, status=f"Ready, approved by Designer on 2026-11-18 against {rev}"))
        self.assertPass(self.p.check("story", "S1"))

    def test_draft_story_stops(self):
        name = self.p.write_report()
        self.p.approve(name)
        (self.p.feature / "tasks.md").write_text(TASKS.format(rev=self.p.rev(), status="Draft"))
        self.assertFailWith(self.p.check("story", "S1"), "not marked Ready")

    def test_story_from_older_revision_stops(self):
        name = self.p.write_report()
        self.p.approve(name)
        (self.p.feature / "tasks.md").write_text(TASKS.format(rev="rev-000000000000", status="Ready, approved against rev-000000000000"))
        self.assertFailWith(self.p.check("story", "S1"), "another spec revision")


class ChangeTests(Base):
    def test_parameter_only_change_is_tuning_and_lists_stories(self):
        old = self.p.spec_text
        self.p.write_spec(reset="05:00")
        res = spec_diff.compare(old, self.p.spec_text)
        self.assertEqual(res["kind"], "tuning")
        self.assertEqual(res["parameters"], ["reset_time"])
        tasks = TASKS.format(rev="x", status="Ready")
        self.assertEqual(spec_diff.affected_stories(tasks, res)[0]["story"], "S1")

    def test_tuning_with_new_date_is_still_tuning(self):
        old = self.p.spec_text
        self.p.write_spec(reset="06:30")
        new = self.p.spec_text.replace("- Last updated: 2026-11-18", "- Last updated: 2026-11-25")
        self.assertIn("2026-11-25", new)
        self.assertEqual(spec_diff.compare(old, new)["kind"], "tuning")

    def test_changed_rule_marks_test_cases(self):
        old = self.p.spec_text
        self.p.write_spec(minutes="20")
        res = spec_diff.compare(old, self.p.spec_text)
        plan = ("# F001 test plan\n\n## Cases\n\n| Case | Rule | Example row | Expect | Status |\n| --- | --- | --- | --- | --- |\n"
                "| TC-F001.claim-once-01 | F001.claim-once | first open | gift shown | Pass |\n"
                "| TC-F001.other-01 | F001.other | x | y | Pass |\n")
        hits = spec_diff.affected_cases(plan, res)
        self.assertEqual([h["case"] for h in hits], ["TC-F001.claim-once-01"])

    def test_rule_change_is_rule_and_names_the_rule(self):
        old = self.p.spec_text
        self.p.write_spec(minutes="20")
        res = spec_diff.compare(old, self.p.spec_text)
        self.assertEqual(res["kind"], "rule")
        self.assertEqual(res["rules"]["changed"], ["F001.claim-once"])

    def test_status_only_change_is_none(self):
        old = self.p.spec_text
        self.p.write_spec(status="Building")
        self.assertEqual(spec_diff.compare(old, self.p.spec_text)["kind"], "none")


class RegisterTests(Base):
    def test_default_location_without_constitution_section(self):
        info = register.where(self.p.root)
        self.assertEqual((info["master"], info["mode"], info["source"]), ("specs/open-questions.md", "local", "default"))

    def test_local_master_named_in_constitution(self):
        section = "## Open questions register\n\n- Master: `specs/questions/register.md`\n- Mode: local\n- Legacy source: none\n\n"
        (self.p.specs / "constitution.md").write_text(CONSTITUTION.format(register=section))
        (self.p.specs / "questions").mkdir()
        self.p.write_register("| OQ-F001-009 | Q | P | Designer | Yes | 2026-11-18 | F001 | |", self.p.specs / "questions" / "register.md")
        self.p.write_report()
        self.assertFailWith(self.p.check("approve"), "OQ-F001-009 is open and blocking")

    def test_legacy_markdown_master_is_read_directly(self):
        legacy = self.p.root / "Docs" / "legacy-register.md"
        legacy.parent.mkdir()
        self.p.write_register("| OQ-F001-004 | Legacy Q | P | Product Owner | Yes | 2026-11-01 | F001 | W99 |", legacy)
        section = "## Open questions register\n\n- Master: `Docs/legacy-register.md`\n- Mode: legacy\n- Legacy source: the old design wiki\n\n"
        (self.p.specs / "constitution.md").write_text(CONSTITUTION.format(register=section))
        self.p.write_report()
        g = self.p.check("approve")
        self.assertFailWith(g, "OQ-F001-004 is open and blocking")
        # resolving it in the legacy master clears the gate
        self.p.write_register("| OQ-F001-005 | Other | P | Designer | No | 2026-11-01 | F001 | |", legacy)
        self.p.write_report(nn="02")
        self.assertPass(self.p.check("approve"))

    def test_unreadable_legacy_master_cannot_verify_ready(self):
        section = "## Open questions register\n\n- Master: https://wiki.example/questions\n- Mode: legacy\n- Legacy source: wiki\n\n"
        (self.p.specs / "constitution.md").write_text(CONSTITUTION.format(register=section))
        self.p.write_report()
        self.assertFailWith(self.p.check("approve"), "cannot verify open questions")
        rows = self.p.root / "rows.tsv"
        rows.write_text("ID\tQuestion\tOwner\tBlocking\tSpec\tStatus\nOQ-F001-007\tQ\tDesigner\tNo\tF001\topen\n")
        self.assertPass(self.p.check("approve", rows_file=rows))

    def test_merge_is_safe_to_repeat_and_never_overwrites(self):
        rows = self.p.root / "rows.tsv"
        rows.write_text("ID\tQuestion\tOwner\tBlocking\tSpec\tWas\n"
                        "OQ-MECH-001\tHow long is rewind?\tDesigner\t\tF004\tMech 9.1\n"
                        "OQ-MECH-002\tInventory size?\tDesigner\tNo\tF008\tMech 9.2\n"
                        "OQ-F001-002\tChanged text\tSomeone\tYes\tF001\t\n")
        path = self.p.specs / "open-questions.md"
        self.assertEqual(register.merge(path, register.rows_from_tsv(rows), "mechanics doc"), (2, 1))
        first = path.read_text()
        self.assertEqual(register.merge(path, register.rows_from_tsv(rows), "mechanics doc"), (0, 3))
        self.assertEqual(path.read_text(), first)
        all_rows = register.rows_from_markdown(first)
        ids = [r["ID"] for r in all_rows]
        self.assertEqual(len(ids), len(set(ids)))
        kept = next(r for r in all_rows if r["ID"] == "OQ-F001-002")
        self.assertEqual(kept["Question"], "Offline?")
        imported = next(r for r in all_rows if r["ID"] == "OQ-MECH-001")
        self.assertEqual((imported["Blocking"], imported["Was"]), ("?", "Mech 9.1"))
        self.assertEqual(imported["section"], "open")

    def test_interrupted_merge_resumes(self):
        rows = self.p.root / "rows.tsv"
        rows.write_text("ID\tQuestion\tOwner\tBlocking\tSpec\nOQ-MECH-001\tA\tDesigner\tNo\tF004\n")
        path = self.p.specs / "open-questions.md"
        register.merge(path, register.rows_from_tsv(rows), "mechanics doc")
        rows.write_text("ID\tQuestion\tOwner\tBlocking\tSpec\nOQ-MECH-001\tA\tDesigner\tNo\tF004\nOQ-MECH-002\tB\tDesigner\tNo\tF008\n")
        self.assertEqual(register.merge(path, register.rows_from_tsv(rows), "mechanics doc"), (1, 1))
        text = path.read_text()
        self.assertEqual(text.count("### Imported from mechanics doc"), 1)
        self.assertEqual(text.count("OQ-MECH-001"), 1)

    def test_next_id_and_check(self):
        rows, _, _ = register.load(self.p.root)
        self.assertEqual(register.next_id(rows, "F001"), "OQ-F001-003")
        self.assertEqual(register.check(rows), [])


class PointerTests(unittest.TestCase):
    def test_pointer_cases(self):
        self.assertEqual(pointer.fixed(""), "@AGENTS.md\n")
        existing = "# My project\n\nKeep this.\n"
        once = pointer.fixed(existing)
        self.assertEqual(once, "@AGENTS.md\n\n# My project\n\nKeep this.\n")
        self.assertEqual(pointer.fixed(once), once)
        dup = "@AGENTS.md\nNotes\n@AGENTS.md\n"
        self.assertEqual(pointer.fixed(dup), "@AGENTS.md\nNotes\n")


class CliFromAnotherDirectory(Base):
    def test_scripts_run_from_a_separate_working_directory(self):
        name = self.p.write_report()
        self.p.approve(name)
        for script, args in (("spec_rev.py", [str(self.p.feature / "spec.md")]),
                             ("ready_check.py", [str(self.p.feature), "--json"]),
                             ("register.py", ["where"])):
            out = subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=self.p.root,
                                 capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        res = json.loads(subprocess.run([sys.executable, str(SCRIPTS / "ready_check.py"), str(self.p.feature), "--json"],
                                        cwd=self.p.root, capture_output=True, text=True).stdout)
        self.assertTrue(res["passed"])


class CarryOverTests(Base):
    def _git(self, *args):
        subprocess.run(["git", "-C", str(self.p.root), *args], check=True, capture_output=True)

    def _approved_and_committed(self):
        self._git("init", "-q")
        self._git("config", "user.email", "t@example.com")
        self._git("config", "user.name", "Test")
        name = self.p.write_report()
        self.p.approve(name)
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "approved")
        commit = subprocess.run(["git", "-C", str(self.p.root), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        return name, commit

    def _carry(self, name, old_rev, commit, **spec_kw):
        self.p.write_spec(status="Ready", **spec_kw)
        new_rev = self.p.rev()
        appr = (f"- Ready: Yes\n- Approved by: Designer\n- Date: 2026-11-19\n- Revision: {new_rev}\n"
                f"- Commit: {commit}\n- Analysis: {name}\n- Carried over: from {old_rev}, tuning only (reset_time)")
        self.p.write_spec(status="Ready", approval=appr, **spec_kw)

    def test_tuning_only_carry_over_passes(self):
        name, commit = self._approved_and_committed()
        old_rev = self.p.rev()
        self._carry(name, old_rev, commit, reset="05:00")
        self.assertPass(self.p.check("ticket"))

    def test_carry_over_of_a_rule_change_is_caught(self):
        name, commit = self._approved_and_committed()
        old_rev = self.p.rev()
        self._carry(name, old_rev, commit, minutes="30")
        self.assertFailWith(self.p.check("ticket"), "rules or other sections changed")


if __name__ == "__main__":
    unittest.main()
