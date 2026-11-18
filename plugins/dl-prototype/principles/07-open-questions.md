# 07. One register of open questions

Every undecided place lives in one register, and every skill reads and writes the same one. Two live registers drift apart within days.

## Where it is

The constitution names it, in its "Open questions register" section:

```markdown
## Open questions register

- Master: `specs/open-questions.md`
- Mode: local
- Legacy source: none
```

- With no such section, the register is `specs/open-questions.md`, in local mode.
- `scripts/register.py where` prints the location every skill uses. Never hard-code the path.

## Two modes

**Local**: the method's file is the master. New questions, answers and triage go there. If an older list existed, its open rows were imported once and the old list is frozen, with a dated note at the top saying so ("Frozen 2026-11-11; open items moved to `specs/open-questions.md` as OQ-MECH-NNN").

**Legacy**: an existing register stays the master (a wiki page, a design doc, a spreadsheet). The Master line names it, as a path or a URL.

- New questions and resolutions go to the legacy register, in its own format.
- If the legacy master is a Markdown file in the method's table format, the scripts read it directly.
- Otherwise the skill reads it, writes its rows to a tab-separated file (ID, Question, Owner, Blocking, Spec, Status), and passes that file to `ready_check.py --register-rows`. The check cannot pass without it.
- If the skill can read the legacy master but cannot write to it, it prepares the exact row or change and reports it as pending, with where it must go. It never claims a question is resolved until the master says so.

## Minimum information per question

| Field | Means | Legacy field it maps from |
| --- | --- | --- |
| ID | Stable, never reused; imported IDs are kept | the legacy ID |
| Question | The decision needed, phrased as a choice where possible | the question text |
| Proposal | The recommended answer, if any | any recommendation in the text |
| Owner | Who decides: a role title | the owner or assignee |
| Blocking | Yes or No against the current milestone; `?` until triaged | rarely recorded: leave `?` |
| Spec | The feature or section it affects | the screen, page or area |
| Was | Where an imported row came from | the source register |

The constitution's register section records how the legacy fields map, when the mode is legacy.

Unknown blocking status stays visible as `?`. The Ready check treats it as not yet triaged and will not pass a feature with one open.

## Writing to the register

- New IDs: `scripts/register.py next-id --feature F003` reads the highest number just before you add one.
- Imports: `scripts/register.py merge --rows rows.tsv --source "<old register>"`. It adds only IDs not already there, never changes an existing row, and can be run again after an interruption without duplicating anything.
- Health: `scripts/register.py check` reports duplicate IDs and open rows with no Blocking value.
- Edit a row with an exact replacement of that row, never a rewrite of the whole file. Another session may have added rows since you read it.
