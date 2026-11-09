---
name: adopt
description: Bring the design-led prototype method into an existing game project that already has code, design docs, tickets or a wiki. Takes stock of what exists, drafts the constitution and glossary from it, imports open questions, and maps old documents to features in specs/sources.md, without rewriting or moving them. Use when adding the method to a game already in development or live. For a brand new game, use the constitution skill.
---

# Adopt

The existing-game start. It reads before it asks, and it changes nothing that already exists: old documents stay where they are, and the method grows around them.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

Read `principles/06-two-starts.md` and `principles/02-who-decides.md` once before starting.

## 1. Take stock (read only)

1. Ask where the project's knowledge lives, if it is not all in this repository: other repos (game code), a wiki, a ticket system, a drive. One question, multiple choice. Ask for read access to the game code or a build too: without it, every Trust value stays Unknown and "Today" sections cannot be checked.
2. List what exists, by kind: design docs, screen or UI specs, flows, technical docs, production docs (scope, schedules, processes), registers (open questions, risks, dependencies), agent or AI setup (`CLAUDE.md`, agent files, rules), and code.
3. For each kind, note the naming scheme, how many there are, and the newest and oldest dates.
4. Do not read every document in full. Read indexes, registers, headings and the most recent of each kind. Large projects have hundreds of documents; sample, then say what was sampled.

## 2. Draft the project layer

Write each file from its template, marked **Status: Draft (adopted)**, with every line sourced from an existing document in brackets, for example `[GDD-001 §2]`. Anything you could not find stays `?` with an open question.

1. `specs/constitution.md`: the game in three lines, pillars, platforms and boundary, out of scope, agent calls, where things live, document prefixes. Existing rules files and `CLAUDE.md` are the best source for agent calls and conventions.
2. `specs/glossary.md`: player words and code words. Look for an existing vocabulary table first, then UI copy and code names. Where the two disagree, add both and raise an open question.
3. `specs/open-questions.md`: **first ask which register is master from now on** (the new file with the old one frozen, or the old one kept and linked). Two live registers drift apart within days. Then import every **Open** question, keeping its original ID when it already follows a scheme and naming the old register in the "Was" column. Group by feature or screen; if the old register has no sections, group by the screen or area in the ID. Do not import resolved ones; link to the old register instead. Add new questions (`OQ-ADOPT-NNN`) for contradictions found in step 1.
   - **More than about 30 open questions:** do not leave them as a flat import. Raise a triage question first: mark Blocking against the current milestone, or bulk-defer what falls outside it. Most old registers record no Blocking flag.
4. `specs/sources.md`: map old documents to features (by feature, then project-wide, then not mapped). Mark Trust as `Unknown` unless you have checked the build or code.
5. `specs/STATE.md`: where the project is now, from the newest production docs and tickets.
6. Empty `specs/features/`, `specs/briefs/`, `specs/overrides/templates/` with a `.gitkeep` each.

## 3. Agent setup, carefully

The project may already have an agent setup. Do not replace it.

- If `AGENTS.md` does not exist, create it from the template.
- If `CLAUDE.md` exists, propose adding `@AGENTS.md` as its first line and show the user the result. Change it only with a yes.
- If the existing setup conflicts with the method, list each conflict and ask how to resolve it, one at a time. Look especially for: agents that make design decisions; rules that forbid cross-document consistency checks (they block `analyze`); a second open questions register; ticket projects named differently in different documents.

## 4. Confirm

Ask the designer to confirm the draft, **one question at a time, as multiple choice with the recommended option first**, in this order:

1. Pillars and out-of-scope (the things most likely to be wrong in old docs)
2. Platforms and boundary
3. Agent calls and ask-first calls
4. Any glossary mismatch
5. The three most important features to spec first: the ones about to change

Business questions go to the owner as `?`, not to the designer.

When confirmed, change the constitution's status to **Agreed** and add a changelog row.

## 5. Report

Tell the user, in under fifteen lines:

- what was found (counts by kind) and what was sampled rather than read
- how many open questions were imported and how many are new
- the disagreements found between documents
- the features recommended to spec first, and that each will be specced only when it is next touched

## Do not

- Move, rename, rewrite or delete existing documents.
- Backfill feature specs for the whole game. A feature gets a spec when it is next changed (`principles/06-two-starts.md`).
- Trust a document over the build. When they disagree, raise it.
- Put old document content into the constitution word for word. Summarise and cite.
