# Changelog

Newest first. Version numbers follow semantic versioning. Bump `plugin.json` and `marketplace.json` together.

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
