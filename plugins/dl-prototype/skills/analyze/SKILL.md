---
name: analyze
description: Check a game feature spec for consistency against the constitution, the glossary, the open questions register and the other feature specs, before it is built or after it changes. Read-only; reports findings. Use before marking a spec Ready, after a spec revision or playtest change, when the constitution changes, or when someone asks whether the specs still hang together.
---

# Analyse

A consistency check across the specs. It reads; it never edits. Findings go to the designer, who resolves or dismisses each one.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For the report template, use `specs/overrides/templates/analysis-report.md` in the project if it exists, otherwise the plugin's `templates/analysis-report.md`.

## Run it as a separate agent

Start one fresh helper agent for the check, so it reads the specs without the reasoning that produced them. Give it only:

- the feature spec to check
- `specs/constitution.md`, `specs/glossary.md`, `specs/open-questions.md`
- the other feature specs it names, and any that share terms, parameters or events with it
- this skill's checklist

It must not read code, tests, tickets, chats or the playtest log. They would fill the spec's gaps, and finding those gaps is the point.

## Checklist

Within the spec:
- Rules that contradict each other, or two rules on one event whose conditions overlap or leave a gap
- Rules with no `Otherwise`, or examples on only one side of the guard
- `?` places with no register row, or blocking rows with no `?`
- Tuning values inside rule text instead of Parameters
- States the rules reach that the States table does not list, and the other way round
- Job stories with no rule behind them, and rules no job story needs

Against the project:
- Conflicts with a design pillar, the out-of-scope list or the platform boundary
- Terms used with a special meaning that are missing from the glossary, or used differently from it
- Other features that share an event, term, parameter or state with this one, and whether this spec changes what they rely on
- Dependencies named as Done that another spec says are not

## Report

1. Write `specs/features/F<NNN>-<name>/analysis-YYYY-MM-DD.md` from `analysis-report.md`. Mark each finding Blocking (a builder would build the wrong thing or stall) or Advisory.
2. Give the user the verdict and the blocking findings in the reply. They resolve each one by editing the spec, or dismiss it with a reason written into the report.
3. A spec with an unresolved blocking finding is not Ready.

## Not checked

Say plainly what this cannot judge: feel, pacing, visual quality, whether it is fun. Those are judged by playing it.
