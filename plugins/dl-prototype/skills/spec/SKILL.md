---
name: spec
description: Write or revise a feature spec for a game feature (the full path of the design-led prototype method). Use when someone describes a new feature, mechanic, system or screen flow they want designed or built, brings a GDD section, ticket or rough idea to turn into a spec, or asks to change an existing feature spec. For a small fix or tweak, use the brief skill instead.
---

# Feature spec

Turns a request in any form (a sentence, a GDD section, a ticket, a pasted design doc) into a feature spec an agent can build from without guessing, and a designer can read in a few minutes.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

Read `principles/04-writing-specs.md` once before the first draft of a session.

## Before writing

1. Read `specs/constitution.md` and `specs/glossary.md`. If there is no constitution, offer to run the `constitution` skill first.
2. Check the size. If the request is one change that fits on a page, suggest the `brief` skill instead and stop unless the user wants a full spec.
3. Search `specs/features/` for a feature this belongs to. Revising an existing spec beats creating an overlapping one.
4. Compare the request with what the specs say happens today, and its words with the glossary. Note every mismatch.
5. Check the request against the design pillars and the constitution's out-of-scope list before writing anything.

## Writing

1. Create `specs/features/F<NNN>-<short-name>/` (next number in the folder) with `spec.md` from `feature-spec.md`.
2. Fill in what the request and the existing specs already say. Do not ask for what you can read.
3. Write rules in the guarded form (When, Provided, Then, Otherwise), each with an ID `F<NNN>.<short-id>` and an examples table with cases on both sides of the guard.
4. Put tuning values in the Parameters table, never inside rule text.
5. Wherever a decision is missing, write `?` and add a row to `specs/open-questions.md`. Mark it Blocking if a builder could not proceed without it.
6. Ask the designer the design questions, **one at a time, as multiple choice with the recommended option first**. Business questions (what the client wants, what a word means for them) are not yours or the designer's to answer: mark them `?`, set the owner to the client or product owner, and move on.
7. Write the playtest hypotheses: what playing it should tell us.
8. Add a changelog row. Keep Status as Draft.

## After writing

- Offer to run `clarify` if there are blocking questions, otherwise `analyze`.
- Offer a plain summary for the client or product owner: what the feature does in plain sentences, with each open question as a concrete case they can answer. The user decides whether it goes to them.

## Revising

1. Read the current spec, its playtest log and its tasks file.
2. Make the change. Keep rule IDs stable; a rule that changes meaning keeps its ID, a new rule gets a new one.
3. Add a changelog row, list tasks or tickets the change affects, and offer to run `analyze`.

## Do not

- Invent design decisions to fill a gap. A visible `?` is better than a confident guess.
- Paste wireframes or mockups into the spec. Link them.
- Change a spec that is In build without telling the user which tasks it affects.
