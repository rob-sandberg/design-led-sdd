---
name: analyze
description: Independent consistency and testability review of a game feature spec against the constitution, the glossary, the open questions register and related specs, recorded against the spec's exact revision. Read-only on the spec; the lead writes the report. Use before a spec is approved as Ready, after any rule or scope change, when the constitution or glossary changes, or when someone asks whether the specs still hang together.
---

# Analyse

A review by a reviewer that has not seen the work. It records what it found and which spec revision it read. It never edits the spec. The designer resolves or dismisses each finding.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/`, `templates/`, `scripts/` and `agents/`. For the report template, use `specs/overrides/templates/analysis-report.md` in the project if it exists, otherwise the plugin's `templates/analysis-report.md`.

## 1. Assemble the inputs (the lead)

1. The spec's revision: `spec_rev.py <spec>`. The commit: `git rev-parse --short HEAD`, or "working copy" if the spec has uncommitted edits.
2. The context revisions: `spec_rev.py specs/constitution.md` and `spec_rev.py specs/glossary.md`.
3. The inputs: the spec; the constitution; the glossary; this feature's rows from the register (`register.py list --feature F<NNN> --json`); every other feature spec this one names or shares a term, parameter, event or state with.
4. Leave out code, tests, assets, tickets, `tasks.md`, briefs, the playtest log, `STATE.md`, chats and earlier analysis reports. They fill the spec's gaps, and finding those gaps is the point.
5. **A rerun after a fix** may be focused: give the reviewer the edited sections, the earlier report's findings they touched, and the rest of the spec for context. Say in the report that it was focused.

## 2. Run the reviewer

Start the plugin's `spec-analyst` agent, in a fresh context, with the inputs' text pasted into its prompt together with the checklist below and the revisions. The agent has Read only; it should need nothing beyond what it was given.

If the `spec-analyst` agent is not available in this Claude Code version, start a fresh general helper with the same prompt and tell it to read nothing else. Then the limit holds by instruction only: write that in the report's Access line.

The reviewer returns findings as a table: number, kind, where (rule ID or section), finding, evidence (quoted text), suggested fix, severity. It does not write files.

## Checklist (give it to the reviewer)

Within the spec:
- Rules that contradict each other, or two rules on one event whose conditions overlap or leave a gap
- Rules with no `Otherwise`, or examples on only one side of the guard
- `?` places with no question ID, or blocking questions with no `?`
- Tuning values inside rule text instead of Parameters
- States the rules reach that the States table does not list, and the other way round
- Job stories with no rule behind them, and rules no job story needs

Testability (the QA view):
- An example row a tester could not set up, or whose outcome could not be observed
- A state with no way in or no way out
- A parameter used but not named in Parameters
- A time or boundary case the examples skip (exactly at the limit, the reset moment, offline, the clock changed)

Against the project:
- Conflicts with a design pillar, the out-of-scope list or the platform boundary
- Terms used with a special meaning that are missing from the glossary, or used differently from it
- Other features that share an event, term, parameter or state with this one, and whether this spec changes what they rely on
- Dependencies named as Done that another spec says are not

Blocking means a builder or tester would build or test the wrong thing, or stall. Everything else is Advisory. Pure wording notes go in a short list, not the findings table. Raise only real defects.

## 3. Write the report (the lead)

1. Name it `specs/features/F<NNN>-<name>/analysis-YYYY-MM-DD-NN.md`, NN the next free run number for that day (01, 02, ...). Never overwrite an earlier report.
2. Fill the header from step 1: spec revision, commit, context revisions, the inputs, and the Access line saying exactly what the reviewer could use.
3. Copy the reviewer's findings unchanged. Leave the Resolutions table empty for the designer's decisions.
4. Check the file is on disk before citing it anywhere.
5. Tell the user the verdict and the blocking findings. The designer resolves each by editing the spec (which makes a new revision, reviewed again before approval) or dismisses it with a reason, recorded in Resolutions with their role and the date.
6. If no blocking finding is left, run `ready_check.py <feature folder> --stage approve`. If it passes, the spec can go to the designer for approval (`principles/03-ready-and-done.md`, "Recording an approval").

## Not checked

Say plainly what this cannot judge: feel, pacing, visual quality, whether it is fun (judged by playing), and whether the build matches the spec (the `build-checker` agent's job).
