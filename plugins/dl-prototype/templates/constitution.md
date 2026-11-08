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

## Agent calls and human calls

- Agents may decide: [naming, file layout, code style, harmless defaults...]
- Ask first: [anything public, anything irreversible, spending, credentials, engine or SDK upgrades, store submissions, real-player data]
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
