---
name: constitution
description: Set up or update a game project for the design-led prototype method. Creates specs/constitution.md, AGENTS.md, the CLAUDE.md pointer, the open questions register, glossary and STATE.md. Use when starting a new game project, adding the method to an existing one, or changing the project's pillars, platforms, boundaries or agent rules.
---

# Constitution

Sets up the project layer of the method, or updates it. The constitution is the one file every agent reads before any other.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

Read `principles/02-who-decides.md` once before starting.

## Setting up a project

1. Check what exists: `specs/`, `AGENTS.md`, `CLAUDE.md`. Never overwrite an existing file; offer to merge instead.
2. Gather what the project already says about itself (README, design docs, an existing CLAUDE.md) and pre-fill from it. Do not ask for what you can read.
3. Ask for what is missing, **one question at a time, as multiple choice with the recommended option first**. Cover, in this order, only what you could not pre-fill:
   1. the game in three lines
   2. design pillars (offer three drafts to choose from or edit)
   3. platforms and engine
   4. what the game relies on but does not build
   5. agent calls versus ask-first calls (offer the template's defaults)
   6. where tickets, design files and published docs live
4. Write:
   - `specs/constitution.md` from `constitution.md`
   - `AGENTS.md` at the repo root from `AGENTS.md`
   - `CLAUDE.md` at the repo root containing `@AGENTS.md` (if a CLAUDE.md exists, add that line at the top and keep the rest)
   - `specs/open-questions.md`, `specs/glossary.md`, `specs/STATE.md` from their templates
   - empty folders `specs/features/`, `specs/briefs/`, `specs/overrides/templates/` (with a `.gitkeep` each)
5. Anything the designer could not answer stays as `?` in the constitution and gets an `OQ-NNN` row in the register.
6. Show the constitution, and ask whether to mark it Agreed.

## Updating

1. Read the current constitution.
2. Make the change the user asked for. Add a changelog row at the top.
3. If the change touches pillars, scope or the boundary, list every feature spec that may now conflict, and offer to run `analyze` on them.

## Keep it short

The constitution should fit on about one screen. If a section grows past a few lines, it probably belongs in a feature spec or a principles doc.
