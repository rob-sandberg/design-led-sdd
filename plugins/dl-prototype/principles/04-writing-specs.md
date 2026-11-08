# 04. Writing specs

Specs here are written for two readers at once: a person who has to understand the design, and an agent that will build from it without asking. Write for the agent's literal reading and the person's quick scan.

## Job stories, not user stories

> **When** [situation or trigger], **I want to** [goal], **so I can** [outcome].

- The **When** is a real situation, not a role. What just happened?
- The **I want to** is a concrete action, not a vague wish.
- The **So I can** names the downstream use.
- One job story per ticket. Two "so I can" clauses means two tickets.

Player-facing stories use the player's situation. Production stories (art, audio, tooling) use the maker's.

## Rules with a guard

A rule says what happens when a condition holds, and what happens when it does not. Writing the second half is where most game bugs are found.

```gherkin
Rule: The daily gift can be claimed once per day
  When      the player opens the gift panel
  Provided  the player has not claimed today's gift
  Then      the claim button is active
  Otherwise the button shows the time until the next gift
```

Below each rule, an **examples table** gives concrete cases on both sides of the guard:

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| first open today | yes | button active | |
| claimed at 09:00, opens at 09:05 | no | "Next gift in 14h 55m" | |

Plain Given/When/Then is fine for acceptance criteria on tickets. Inside feature specs, prefer the guarded form: it is what the production tier uses, so a feature that graduates needs no rewrite.

## Undecided places

Mark anything not yet decided with `?` inline, and add a matching row to `specs/open-questions.md`. A spec may hold `?` while it is Draft. Nothing with a blocking `?` is built.

## Conventions

- **Open question IDs:** `OQ-<feature ID>-NNN` (for example `OQ-F003-002`), or `OQ-NNN` for project-wide questions. Columns: ID, Question, Owner, Blocking, Status. Status is `Open`, `Resolved: <answer>` or `Deferred`.
- **Changelog rows:** `YYYY-MM-DD | what changed | who`. Newest row at the top.
- **Risks:** "If [condition], then [consequence]." in sentence case.
- **Numbering:** within a prefix group, take the highest number and add one. Numbers 90 to 99 are reserved for permanent bottom items (indexes, registers).
- **Vocabulary:** if the game's words differ from the code's words, keep both in the glossary. Agents use the code word in code and the game word in anything a player sees.
- **Authorship:** documents a client or outside team reads use role titles, never agent names.
- **Links:** every handover card or ticket that refers to a spec links to it at the top.

## Size

- One feature per folder. If a feature's rules split into groups that share no term and no event, it is two features.
- Keep `constitution.md` short enough to read in a minute. Every agent reads it.
- Visual detail (wireframes, mockups, motion) lives in design files or prototypes and is linked, not pasted.
