---
name: tasks
description: Break an approved (Ready) game feature spec into job stories with Gherkin acceptance criteria traced to rule IDs, per-discipline tasks and a QA test plan, ready to paste or push into Jira, GitHub Issues or another ticket system. Verifies the Ready gate first and stops if it fails. Use when a spec is Ready and the team needs tickets, or when someone asks for stories, tickets or a task breakdown for a feature.
---

# Tasks

Turns an approved spec into stories, tasks and a test plan. The spec stays the source of truth; every story, scenario and test case traces to a rule ID and to the spec revision it was written from.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/`, `templates/` and `scripts/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`. Read `principles/03-ready-and-done.md` once.

## 1. Check the gate before writing anything

Run `ready_check.py specs/features/F<NNN>-<name> --stage ticket`. Write nothing and post nothing unless it passes. On a failure, say why and route it:

| The check says | Send it to |
| --- | --- |
| No analysis report, or the report reviewed an older revision | `analyze`, then the designer's approval |
| A blocking or untriaged question is open | `clarify` |
| The prerequisites pass but the designer has not approved, or the approval names an older revision | Ask the designer to approve (one question), then record it |
| A blocking finding is unresolved | The designer: edit the spec or dismiss with a reason |

A Status line that says Ready is not enough: the check reads the Approval section.

## 2. Write the stories (Draft)

1. Ask which slice to ticket, if the spec is large. Recommend the smallest slice that can be played.
2. Write `specs/features/F<NNN>-<name>/tasks.md` from `tasks.md`, headed with the spec revision, the approver and the commit:
   - One story per job story in the slice, each with `**Status:** Draft`. Keep the spec's wording.
   - Each story lists the rule IDs it implements.
   - Acceptance criteria as Gherkin scenarios, each naming the rule and example row it comes from: happy path, guard (the `Otherwise` side), error. Take them from the rules' examples tables; do not invent new behaviour.
   - Tasks per discipline with dependencies.
   - "Proved by": how the designer or QA will play it on the target to call it done.
   - "Not ticketed": what the slice leaves out.
3. Fill the Universal Ready table for each story. List any that fail and why.
4. **Shift QA left.** Draft `test-plan.md` from `test-plan.md`: one case per example row the slice covers, ID `TC-<rule ID>-NN`, with its kind (Happy, Guard, Error, Boundary), set-up and expected outcome taken from the row. If no test room exists for the feature, draft `test-room.md` with a spawn or marker for each case's set-up; the designer or QA approves the room before the stories that use it are built. If `summary.md` is missing, write it, so a tester can start on the feature without a briefing. QA owns the test plan from here.

## 3. Story approval

The test room, if drafted, is approved in the same pass, before the stories that use it.

Ask the designer, one story at a time, multiple choice: approve as Ready, approve with the listed risks accepted, or not yet. On a yes, set the story's Status line to `Ready, approved by <role> on <date> against <revision>`.

## 4. Post tickets (only Ready stories)

For each story to post, run `ready_check.py <feature folder> --story S<n>`. Post only stories that pass, to the ticket system the constitution names, if a connector or CLI is available and the user says yes. Link each ticket to the spec and quote the revision. Write the ticket keys back into `tasks.md`. Use role titles, never agent names, in ticket text. When testing the method, keep tickets local: write them to `tasks.md` only.

## Do not

- Write or post tickets when the check fails, whatever the Status line says.
- Add acceptance criteria the spec does not support. If a story needs a rule the spec lacks, raise an open question and leave that part out.
- Write user stories ("As a..."). Job stories only.
