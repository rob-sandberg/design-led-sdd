# Constitution: [GAME NAME]

- Status: Draft | Agreed
- Owner: [role title]
- Last updated: YYYY-MM-DD

Every agent reads this first. Keep it to about one screen. Detail belongs in specs; this file holds what is true across all of them.

## The game in three lines

[What it is, who it is for, what makes it worth playing.]

## Design pillars

1. [Pillar]: [one line on what it rules in and rules out]
2. [Pillar]: [...]
3. [Pillar]: [...]

## Platforms and boundary

- Platforms: [iOS, Android, Steam, console...]
- Engine and stack: [Unity 6 UI Toolkit, Godot 4, Supabase...]
- Relied on, not built: [engine, store billing, ad SDK, backend service...]. Agents treat these as given and do not test their failures, except where a spec says otherwise.

## Out of scope for the game

- [Things this game will not do, ever, not just this milestone.]

## Roles

The method's roles and the titles they have here. Skills and templates use the method's names; anything an outside reader sees uses the titles.

| Method role | Decides | Title here |
| --- | --- | --- |
| Designer | Design calls, every design gap, playtest conclusions; approves Ready for specs and stories | [e.g. Creative Director] |
| Product owner | Business questions: what the game should do, what a word means, scope | [...] |
| Producer | Priority, milestone scope, what is ready and done | [...] |
| QA | Test evidence; raises testability gaps as open questions | [e.g. QA Lead] |

One person may hold several roles.

## Agent calls and human calls

- Agents may decide: [naming, file layout, code style, harmless defaults, and process or housekeeping that changes no game rule, no spec's meaning and no constitution text]. Agents list each such call in one line when they finish, so it can be undone.
- Ask first: [marking a spec or story Ready (always the designer's), any change to a spec's rules or this constitution, anything public, anything irreversible, spending, credentials, engine or SDK upgrades, store submissions, real-player data]
- Never: [...]

## Ready and done additions

Additions to the universal lines in the method's principles, per discipline.

- UI design: [...]
- Art: [...]
- Engineering: [...]
- QA: [...]

## Where things live

| What | Where |
| --- | --- |
| Specs | `specs/` |
| Design files | [Figma link] |
| Tickets | [Jira project key / board] |
| Published docs | [Confluence space / none] |
| Builds | [how to build, how to get on device] |
| Open questions | See "Open questions register" below |

## Open questions register

The one place undecided questions live. Every skill reads this section to find it (`scripts/register.py where`). See the method's principle `07-open-questions.md`.

- Master: `specs/open-questions.md`
- Mode: local
- Legacy source: none

For a legacy master (mode `legacy`), add one line per mapped field, for example `- Field map: Ref → ID, Detail → Question, Assignee → Owner, Screen → Spec`.

## Document prefixes

| Prefix | Means |
| --- | --- |
| F | Feature spec folder |
| B | Brief |
| OQ | Open question |
| [add project prefixes] | |

## Changelog

| Date | Change | By |
| --- | --- | --- |
| YYYY-MM-DD | First version | [role] |
