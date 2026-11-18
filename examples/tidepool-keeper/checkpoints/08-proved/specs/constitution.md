# Constitution: Tidepool Keeper

- Status: Agreed
- Owner: Lead Designer
- Last updated: 2026-11-18

Every agent reads this first. A fictional project, built to show the method.

## The game in three lines

A cosy mobile game about keeping a tidepool alive. For players who want five calm minutes a day. Worth playing because the pool changes a little every time you come back.

## Design pillars

1. **Calm, never nagging**: the game invites, it does not punish. Rules out streaks that reset to zero, timers that shame, and push reminders by default.
2. **One-tap moments**: the daily things take one tap. Rules out menus between the player and a gift.
3. **The pool remembers**: what you did yesterday shows today. Rules out content that ignores the player's history.

## Platforms and boundary

- Platforms: iOS and Android, free to play.
- Engine and stack: Unity 6, a small game server for time and claims.
- Relied on, not built: Unity, the app stores, the game server's clock.

## Out of scope for the game

- Paying to recover anything missed.
- Push notifications in the first release.

## Roles

| Method role | Decides | Title here |
| --- | --- | --- |
| Designer | Design calls, every design gap, playtest conclusions; approves Ready for specs and stories | Lead Designer |
| Product owner | Business questions: what the game should do, what a word means, scope | Product Owner |
| Producer | Priority, milestone scope, what is ready and done | Producer |
| QA | Test evidence; raises testability gaps as open questions | QA Lead |

## Agent calls and human calls

- Agents may decide: naming, file layout, code style, harmless defaults, and process or housekeeping that changes no game rule, no spec's meaning and no constitution text. Agents list each such call in one line when they finish.
- Ask first: marking a spec or story Ready, any change to a spec's rules or this constitution, anything public, spending.
- Never: answer a design or business question on someone's behalf.

## Ready and done additions

- QA: every case in the test plan is Pass, or Blocked with a reason the Lead Designer accepted.

## Where things live

| What | Where |
| --- | --- |
| Specs | `specs/` |
| Tickets | `tasks.md` in each feature (kept local in this example) |
| Builds | Android emulator, then a phone |
| Open questions | See "Open questions register" below |

## Open questions register

- Master: `specs/open-questions.md`
- Mode: local
- Legacy source: none

## Document prefixes

| Prefix | Means |
| --- | --- |
| F | Feature spec folder |
| B | Brief |
| OQ | Open question |
| TC | Test case |

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-11-18 | Agreed | Lead Designer |
