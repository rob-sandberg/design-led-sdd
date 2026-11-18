# Changelog

Newest first. Version numbers follow semantic versioning. Bump `plugin.json` and `marketplace.json` together.

## dl-prototype 0.3.0 (2026-11-18)

Lessons from a week on a real Unity project, and an outside review. The two key behaviours are now scripts with tests.

**Ready, twice**

- Every spec has a revision (`rev-` plus 12 hex characters) from its design content; status, dates, approval and changelog are left out.
- `scripts/ready_check.py` checks a spec at three stages: approve, ticket and story. It explains each failure in a plain line. Exit 0 pass, 1 fail.
- Analysis reports name the revision and context they read, and are numbered `analysis-YYYY-MM-DD-NN.md`. A report on an older revision no longer counts. Blocking findings are dismissed with a reason and who decided, or fixed and rechecked.
- The designer approves the spec, then each story. The spec template has an Approval section; agents fill it only after an explicit yes.
- `scripts/spec_diff.py` says whether a change is tuning (Parameters only) or a rule change, and lists the stories and test cases it touches. A rule change lapses the approval; a tuning change can carry it over.

**Open questions**

- One register, named in the constitution (default `specs/open-questions.md`), local or legacy mode. New principle `07-open-questions.md`.
- `scripts/register.py` finds the register, gives the next ID, and merges imports by ID without overwriting.
- A Proposal column; Blocking can be `?` until triaged, and the Ready check treats that as blocking.

**Shift-left QA**

- QA is a role in `02-who-decides.md` and joins at Clarify; testability is on the analysis checklist.
- New templates: `test-plan.md` (one case per example row), `test-room.md` (approved before the build), `summary.md` (for readers outside the team).
- New agents: `spec-analyst` (Read only, reviews pasted inputs) and `build-checker` (maps rules to code and tests, changes nothing).

**Other**

- Constitution: a Roles table maps method roles to the team's titles; agents may make process and housekeeping calls that change no game rule, listed in one line.
- Changelog rows say who decided and who applied the change.
- `scripts/pointer.py` keeps exactly one `@AGENTS.md` line in `CLAUDE.md`; `adopt` keeps an existing AGENTS.md and is safe to rerun.
- Tidepool Keeper is now ten checkpoints, one per step, built by `tools/make_fixture.py`; the worked example follows them.
- Tests: `python3 -m unittest discover -s tests`.

## Repository (2026-11-11)

- Loop diagram (`docs/dl-prototype-loop.svg`, PNG), now in the method guide.
- Design notes: the decisions behind the method, what was taken from Spec Kit and Proviso, the adopt trial lessons.
- PDFs of the method guide, worked example and design notes.
- Diagram scripts in `tools/`.

## Repository (2026-11-10)

- Landing page for GitHub Pages (`docs/index.html`), with HTML versions of the guides.
- Method guide, worked example, cheat sheet (HTML, PDF, PNG) and method flow (SVG, PNG) included in `docs/`.
- `tools/build_docs.py` rebuilds the guide pages from Markdown.

## dl-prototype 0.2.1 (2026-11-09)

Fixes from the first `adopt` trial on a real project (about 130 documents, 170 open questions):

- `adopt` asks which open questions register is master before importing.
- Keeps existing question IDs; groups by screen or area when the old register has no sections.
- Large imports (over about 30 open questions) start with a triage question.
- Asks for code or build access up front, so Trust can be checked.
- Looks for setup conflicts that block the method, such as rules forbidding consistency checks.

## dl-prototype 0.2.0 (2026-11-09)

- Two starts: `constitution` is now the new-game start; new `adopt` skill for existing games.
- New principle `06-two-starts.md`: spec the change, not the game; the build beats the document.
- New template `sources.md`: old documents mapped to features, with trust and disagreements.
- `spec` fills "Today" from the build and old documents when a feature already exists.
- Open questions register gains a "Was" column for imported IDs.

## dl-prototype 0.1.0 (2026-11-08)

- First version.
- Principles: the loop, who decides, ready and done, writing specs, two tiers.
- Templates: constitution, AGENTS.md, feature spec, brief, tasks, playtest log, open questions, glossary, STATE, analysis report.
- Skills: constitution, spec, brief, clarify, analyze, tasks, playtest.
- Example: Tidepool Keeper, feature F001.
