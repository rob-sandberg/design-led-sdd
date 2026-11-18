# 03. Ready and done

The minimum bar. If a piece of work does not meet Ready, it stays in the queue. If it does not meet Done, it does not move to Done. Work that fails review does not move backwards: raise a new item for the rework.

Ready is given twice: once for the feature spec, then once for each story after `tasks` writes it. Both are the designer's decision, recorded with the spec revision they approved.

## Spec revision

Every spec has a **revision ID**, printed by `scripts/spec_rev.py`: a short hash of its design content, such as `rev-3f9a1c0d2b7e`. It ignores the Status and Last updated lines, the Approval section and the Changelog, so recording an approval or moving the status keeps the same ID. Any edit to intent, scope, job stories, rules, examples, states, parameters, terms or any other section gives a new one. A date or a branch name is never a revision.

Analysis reports, the spec's Approval section, `tasks.md` and each story record the revision they were written against, plus the git commit when there is one.

## The Ready check

One check, the same whichever skill runs it (`clarify`, `analyze`, `spec`, `tasks`, `playtest`). Run it with `scripts/ready_check.py <feature folder>`; it says PASS or FAIL and why.

**Before asking the designer to approve** (`--stage approve`):

1. Intent, player experience and scope are written, not template text.
2. Every rule has an ID, an `Otherwise`, and examples on both sides of the guard.
3. Every term the spec defines is in the glossary.
4. No open question for this feature is blocking, or has no Blocking value. Unknown blocking status needs triage before Ready.
5. Every `?` left in the spec cites a question that is not blocking. A `?` with no question ID is a warning to raise one.
6. The latest analysis report reviewed the **current revision**, and the constitution and glossary have not changed since it was written. When they have, a context recheck is enough: a short report on the same spec revision saying which findings or rules the change touches, if any.
7. Every blocking finding in that report is resolved. A blocker fixed by an edit changes the revision, so the edited spec is checked again before approval; a rerun may cover only the edited parts and the findings they touched. A dismissed blocker names who decided and why. Advisory findings may stay open; they stay visible in the report.

**Before tickets are written or posted** (`--stage ticket`): all of the above still passes, and the Approval section records `Ready: Yes`, the approver, the current revision and the latest report.

**Before a story is built** (`--story S1`): the ticket stage passes, and the story's status is Ready against the current revision.

If the check cannot read the open-questions register, it cannot pass. See `07-open-questions.md`.

## Recording an approval

Whichever skill reaches a passing approve-stage check asks the designer, one question, multiple choice: approve as Ready, or not yet. Only on an explicit yes:

1. Fill the spec's Approval section: `Ready: Yes`, approved by (the designer's role title), date, the revision from `spec_rev.py`, the commit (`git rev-parse --short HEAD` if the spec is committed, else "working copy"), and the latest report's file name.
2. Set the Status line to Ready and add a changelog row: "Ready (Designer), against rev-…; N advisory findings left open".
3. Run the ticket-stage check to confirm it passes.

Story approval works the same way in `tasks.md`: the designer approves each story, and its Status line records the approver, date and spec revision.

An agent never writes an approval the designer did not give, and never carries one over without the designer's yes.

## When the spec changes after approval

- **Rule or scope change** (from `spec`, `playtest` or an answered question): the revision changes, so approval lapses on its own. Set the status back to Draft. Run `scripts/spec_diff.py <spec> --since <approved commit> --tasks <tasks.md>` to list the rules that changed and the stories that cite them. Mark those stories for recheck, and the test cases that cite a changed rule as Stale (`--test-plan <test-plan.md>` lists them). Work already in progress keeps its record and status; nothing is deleted. The changed spec goes through analysis and the designer's approval again before new or revised work is handed off.
- **Parameter-only change** (tuning): `spec_diff.py` reports the kind as `tuning`. Approval may be carried over to the new revision without a new analysis when the stories that name the parameter still pass their acceptance criteria as written and no other feature relies on the old value. The designer records the carry-over in the Approval section (new Revision, plus `- Carried over: from rev-…, tuning only (<parameters>)`) and the changelog. The Ready check then accepts the earlier report, and when the approval names a commit it confirms with `spec_diff.py` that only parameters changed. If an acceptance criterion or another feature depends on the value, say so and recheck as for a rule change.
- **Status, dates, approval or changelog only**: no design change; nothing lapses.

## Universal Ready (any task or ticket)

1. Title follows the project's naming convention
2. It links to its spec or brief, and to the spec revision
3. Acceptance criteria are written: at least three points, describing what, not how
4. Its parent story is linked (tasks only)
5. Dependencies on other disciplines are named and either done or explicitly accepted as a risk

## Universal Done

1. All acceptance criteria are met and verified on the target
2. Reviewed by at least one other person (or a separate checking agent, for agent work)
3. No known defect blocks the next discipline in the chain
4. A one-sentence completion note says what was delivered
5. Any decision or deviation from the spec is written into the spec or raised as an open question

## Story Done

1. All its tasks are Done
2. The player can do what the job story says, in a playable build
3. A designer or producer has played it, not just ticked the tasks
4. Its happy path, guard and error scenarios all pass, each traced to the rule it proves

## Discipline additions

Add discipline-specific Ready and Done lines in the project constitution (section "Ready and done additions"). Typical ones:

- **UI design:** all screen states documented (default, empty, loading, error, edge cases)
- **Art:** assets exported to the agreed format and committed to the agreed place
- **Engineering:** no regressions; reviewed by a second engineer or checking agent
- **QA:** pass or fail per acceptance criterion, with the build version tested
