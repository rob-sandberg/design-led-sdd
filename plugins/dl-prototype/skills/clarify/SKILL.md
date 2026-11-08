---
name: clarify
description: Work through the open questions and undecided places (?) of a game feature spec until it can be marked Ready. Use when a spec has blocking open questions, when someone asks what is still undecided, when answers come back from a client or product owner, or before breaking a spec into tasks.
---

# Clarify

The gate between Draft and Ready. A feature spec cannot be marked Ready while a blocking open question is Open.

## Steps

1. Read the spec, `specs/open-questions.md` and `specs/glossary.md`.
2. List every `?` in the spec and every Open row for this feature. Flag any `?` with no register row, and any row whose `?` is gone from the spec.
3. Look for gaps the spec has not marked yet. Use the checklist below. Raise each one as a new open question.
4. Sort the questions:
   - **Design questions** (the designer answers now)
   - **Business questions** (the client or product owner answers; not yours or the designer's)
   - **Production questions** (the producer answers: scope, priority, milestone)
5. Ask the designer's and producer's questions **one at a time, as multiple choice with the recommended option first**. After each answer, write it into the spec, remove the `?`, and move the register row to Resolved with the answer and who decided.
6. For business questions, draft a short note for the owner: each question as a concrete case ("A player claims at 23:59 and opens the panel at 00:01. Should they see a new gift?"), with the options. The user decides whether to send it.
7. When answers come back from the owner, fold them in the same way.
8. If no blocking question is left, offer to run `analyze`, then mark Ready.

## Gaps to look for

- A rule with no `Otherwise`, or an `Otherwise` that says nothing a builder could test
- An examples table with cases on only one side of the guard
- Boundaries: exactly at the limit, just under, just over, zero, the maximum
- Time: midnight, time zones, the app closed or backgrounded, the clock changed by the player
- Interruptions: no network, app killed mid-action, purchase or ad failing halfway
- Two rules on the same event whose conditions overlap or leave a case uncovered
- State the rule depends on but the spec never says where it comes from
- A word used with a special meaning that is not in the glossary
- An outcome only one way of building it would produce (the spec is describing an implementation)
- A tuning value written inside a rule instead of the Parameters table

## Do not

- Answer a question on the owner's behalf, even when the answer seems obvious. Recommend; do not decide.
- Mark a spec Ready yourself. The designer does.
