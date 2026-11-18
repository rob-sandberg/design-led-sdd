# F[NNN]: [Feature name], test plan

- Owner: QA
- Written from: spec revision rev-xxxxxxxxxxxx (stories S1 to S[n] in `tasks.md`)
- Test room: `test-room.md`
- Last run: [build or commit], YYYY-MM-DD

A tester can start here with no other briefing: read `summary.md` for what the feature is, this file for what to check, and `test-room.md` for where. Every case comes from an example row in the spec; none adds behaviour. If the spec's revision changes, cases citing a changed rule are marked Stale until rechecked.

## Cases

| Case | Rule | Example row | Set-up (room, spawn, state) | Do | Expect | Kind | Status | Build | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-F[NNN].[rule-id]-01 | F[NNN].[rule-id] | [the row's situation] | [spawn a, gift waiting] | [the action] | [the row's outcome] | Happy / Guard / Error / Boundary | Not run / Pass / Fail / Blocked / Stale | | |

- **Kind**: Happy (the guard holds), Guard (the Otherwise side), Error (interruption, offline, failure), Boundary (exactly at a limit, the reset moment, zero, the maximum).
- **Blocked**: the case cannot be run yet (missing art, a dependency not built). Say what blocks it.
- **Fail**: raise a bug linked to the case and the rule. If the build is right and the spec is wrong or silent, raise an open question instead.

## Not covered by this plan

- Feel, pacing and fun: judged in playtests (`playtest-log.md`), not here.
- [Rules or rows outside the ticketed slice, by ID.]

## Run log

Newest first.

| Date | Build | Who | Cases run | Pass | Fail | Blocked | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
