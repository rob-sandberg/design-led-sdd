# F001: Daily tide gift, playtest log

## Session 1: 2026-11-24

- Build: 0.1.7
- Who played: six internal players, one week
- What we tested: hypotheses 1 and 2 (the Streak was not in the build, so no Streak hypothesis was tested)

### Decision rules, written before the results

| # | Hypothesis | Held if | Failed if |
| --- | --- | --- | --- |
| 1 | Players claim on their first visit to the beach each day | 4 or more of 6 players, on most days | 2 or fewer |
| 2 | Few players meet a countdown on their first open | no more than 1 player of 6 | 2 or more |

### What we saw

Observations:

- Four of six players claimed on their first beach visit on five of the seven days.
- Two players opened the beach before 05:00 on most days and saw only a countdown.
- No player opened the beach a second time on the same day to check the countdown.

Opinions (recorded, not acted on alone):

- One player said a reminder would help. This challenges the pillar "Calm, never nagging"; flagged to the Lead Designer, no change.

### Hypotheses

| # | Result | Evidence |
| --- | --- | --- |
| 1 | Held | 4 of 6 on five of seven days |
| 2 | Failed | 2 of 6 opened before the Reset on most days |

### Spec changes

| Spec part | Change | Kind | Decided | Effect on approval |
| --- | --- | --- | --- | --- |
| Parameter `reset_time` | 05:00 to 04:00 | Tuning | Lead Designer, 2026-11-25 | Carried over: S1's scenarios name `reset_time`, not a clock time; no other feature uses it. Three test cases rerun |
| Job story 2 and F001.claim-once's Otherwise | Countdown dropped; the empty shell instead | Rule | Lead Designer, 2026-11-26 | Approval lapsed: back through analyze and approval; S1 to Recheck |
| Pillar "Calm, never nagging" | One request for reminders | Pillar | Flagged, no change | None |

### Next session tests

1. With `reset_time` at 04:00, does any player meet the empty shell on a first open?
