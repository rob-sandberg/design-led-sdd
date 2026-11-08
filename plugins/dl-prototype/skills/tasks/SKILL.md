---
name: tasks
description: Break a Ready game feature spec into job stories with Gherkin acceptance criteria and per-discipline tasks, ready to paste or push into Jira, GitHub Issues or another ticket system. Use when a spec is Ready and the team needs tickets, or when someone asks for stories, tickets or a task breakdown for a feature.
---

# Tasks

Turns a Ready spec into stories and tasks in a standard handover format. The spec stays the source of truth; tickets link back to it.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`. Read `principles/03-ready-and-done.md` once.

## Steps

1. Read the spec, the constitution and the glossary.
2. Check the spec is Ready. If it is Draft, or has an Open blocking question, stop and offer `clarify`. If `analyze` has not run on its current state, offer to run it first.
3. Ask which slice to ticket, if the spec is large: all of it, or a first playable slice. Recommend the smallest slice that can be played.
4. Write `specs/features/F<NNN>-<name>/tasks.md` from `tasks.md`:
   - One story per job story in the slice. Keep the spec's wording.
   - Each story lists the rule IDs it implements.
   - Acceptance criteria as Gherkin scenarios: happy path, guard (the `Otherwise` side), error. Take them from the rules' examples tables; do not invent new behaviour.
   - Tasks per discipline with dependencies (design before art before engineering, unless the constitution says otherwise).
   - "Proved by": how a designer or producer will play it to call it done.
   - "Not ticketed": what the slice leaves out.
5. Check each story against Universal Ready. List any that fail and why.
6. Ask whether to push them to the ticket system named in the constitution. If yes and a connector or CLI is available, create them, link each to the spec, and write the ticket keys back into `tasks.md`. Use role titles, never agent names, in ticket text.

## Do not

- Add acceptance criteria the spec does not support. If a ticket needs a rule the spec lacks, raise an open question and leave the ticket out.
- Write user stories ("As a..."). Job stories only.
