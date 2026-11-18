---
name: clarify
description: Work through the open questions and undecided places (?) of a game feature spec, route each decision to its owner, and take the spec to the designer's Ready approval once the Ready check passes. Use when a spec has blocking or untriaged open questions, when someone asks what is still undecided, when answers come back from a client or product owner, or before breaking a spec into tasks.
---

# Clarify

Resolves or routes every open decision on a feature, then hands the spec on: to `analyze` if the review is missing or out of date, or to the designer for Ready approval when the Ready check passes.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/`, `templates/` and `scripts/`. Run scripts with `python3 <plugin>/scripts/<name>.py` from the project root. Read `principles/03-ready-and-done.md` and `principles/07-open-questions.md` once before starting.

## Steps

1. Find the register: `register.py where`. Read the spec, the glossary and the register rows for this feature (`register.py list --feature F<NNN>`). If the register cannot be read, say so: nothing about Ready can be verified until it can.
2. List every `?` in the spec and every open row for this feature. Flag a `?` with no question ID on its line, and a row whose `?` is gone from the spec.
3. Look for gaps the spec has not marked yet, using the checklist below. Raise each as a new question with the next ID (`register.py next-id --feature F<NNN>`), a Proposal, an owner and a Blocking value.
4. Triage every row with Blocking `?`: ask the producer, one question, multiple choice, whether it blocks the current milestone.
5. Sort the questions by who decides (roles in the constitution):
   - **Design questions**: the designer answers now.
   - **Business questions**: the product owner answers; not yours or the designer's.
   - **Production questions**: the producer answers (scope, priority, milestone).
   - **Testability questions**: QA raises them; the designer answers.
6. Ask the designer's and producer's questions **one at a time, as multiple choice with the recommended option first**. After each answer, write it into the spec, remove the `?`, and move the row to Resolved with the answer, who decided and the date. In legacy mode, write the change to the legacy master, or prepare it exactly and report it as pending.
7. For business questions, draft a short note for the owner: each question as a concrete case ("A player claims at 23:59 and opens the panel at 00:01. Should they see a new gift?"), with the options. The user decides whether to send it. Fold answers in the same way when they come back.
8. Run the Ready check: `ready_check.py specs/features/F<NNN>-<name> --stage approve`.
   - **Fails only on analysis** (no report, or the report reviewed an older revision): run `analyze` now, or hand it over if the user prefers. Come back to step 8 when it has finished.
   - **Fails on anything else**: report what is left, and stop.
   - **Passes**: ask the designer to approve the spec as Ready, then record it as `principles/03-ready-and-done.md` describes under "Recording an approval".

## Gaps to look for

- A rule with no `Otherwise`, or an `Otherwise` that says nothing a builder or tester could check
- An examples table with cases on only one side of the guard
- Boundaries: exactly at the limit, just under, just over, zero, the maximum
- Time: midnight, the reset moment exactly, time zones, the app closed or backgrounded, the clock changed by the player
- Interruptions: no network, app killed mid-action, purchase or ad failing halfway
- Two rules on the same event whose conditions overlap or leave a case uncovered
- State the rule depends on but the spec never says where it comes from
- A case a tester could not set up or could not observe
- A word used with a special meaning that is not in the glossary
- An outcome only one way of building it would produce (the spec is describing an implementation)
- A tuning value written inside a rule instead of the Parameters table

## Do not

- Answer a question on the owner's behalf, even when the answer seems obvious. Recommend; do not decide.
- Write an approval the designer did not give.
- Keep a second list of questions anywhere but the register the constitution names.
