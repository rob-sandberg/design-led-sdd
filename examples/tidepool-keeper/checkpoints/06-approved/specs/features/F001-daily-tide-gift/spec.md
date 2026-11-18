# F001: Daily tide gift

- Status: Ready
- Owner: Lead Designer
- Last updated: 2026-11-19
- Links: tasks: `tasks.md` · test plan: `test-plan.md` · test room: `test-room.md` · summary: `summary.md`

## Intent

Give lapsed players a reason to open the game once a day, without punishing them for missing one. Serves the pillars "Calm, never nagging" and "One-tap moments".

## Player experience

The player opens the game and the tide has left something on the beach. Claiming it is one tap and feels like a small surprise. Missing a day should feel like nothing was lost.

## Today

Nothing. There is no daily reward.

## Scope

- In: one tide gift per day; the time until the next one; a streak that never falls to zero.
- Out, for now: gifts the player chooses; push notifications.
- Out, for good: paying to claim a missed day.

## Job stories

1. When I open the game for the first time today, I want to collect what the tide left, so I can feel the game noticed I came back.
2. When I have already collected today's gift, I want to see when the next one arrives, so I can decide whether to come back tomorrow.

## Rules

### F001.claim-once: The tide gift can be claimed once per day

```gherkin
When      the player opens the beach
Provided  the player has not claimed since the last Reset
Then      the tide gift is on the beach and one tap claims it
Otherwise the beach shows the time until the next Reset
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| last claim yesterday at 09:00; opens today exactly at `reset_time` | yes | tide gift shown | the Reset has just passed |
| last claim yesterday at 09:00; opens today one minute before `reset_time` | no | countdown "Next tide in 1m" | the Reset is a minute away |
| claimed today at 09:00; opens today at 09:10 | no | countdown to the next `reset_time` | already claimed since the Reset |
| last claim yesterday; opens after the Reset | yes | tide gift shown, its contents drawn from `gift_table` | the gift's contents are a parameter |

### F001.server-time: The game server decides whether the Reset has passed

```gherkin
When      the player taps the tide gift
Provided  the game server agrees the last Reset is later than the player's last claim
Then      the claim is accepted and the gift goes into the pool
Otherwise the claim is refused and the beach shows the time to the next Reset, by the server's clock
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| claimed today at 09:00; sets the phone clock forward a day and taps | no | refused; countdown by the server's clock | the server's clock decides (OQ-F001-002) |
| last claim yesterday; taps after the Reset | yes | claim accepted | the server agrees |

### F001.streak-floor: A missed day lowers the Streak by `streak_penalty`, never to zero

```gherkin
When      the player claims a tide gift
Provided  the player also claimed in the previous day
Then      the Streak goes up by one
Otherwise the Streak goes down by `streak_penalty`, to no lower than `streak_floor`
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| Streak 4, claimed yesterday | yes | Streak 5 | |
| Streak 4, missed yesterday | no | Streak 3 | |
| Streak 1, missed three days | no | Streak 1 | never below `streak_floor` |

### F001.offline: With no connection, the shell waits

```gherkin
When      the player opens the beach
Provided  the game has a connection to the game server
Then      F001.claim-once decides what the beach shows
Otherwise the shell is greyed, with "Tide is out", and cannot be tapped
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| online; not claimed since the Reset | yes | tide gift shown | F001.claim-once applies |
| no connection; not claimed since the Reset | no | greyed shell, "Tide is out" | a claim needs the server (OQ-F001-003) |

## States

| State | What the player sees | How they get here | How they leave |
| --- | --- | --- | --- |
| Gift waiting | A shell on the beach, glowing | First open after the Reset | Taps the shell |
| Claimed | The gift card, then the time to the next tide | Taps the shell | Closes the card |
| Waiting | The empty shell, with the time to the next tide | Already claimed since the Reset | The next Reset |
| Offline | The shell greyed, "Tide is out" | Opens the beach with no connection | The connection returns |

## Parameters

| Name | Value | Unit | Notes |
| --- | --- | --- | --- |
| reset_time | 05:00 | player's local time | *start*; early, so late players are not cut off at midnight |
| streak_penalty | 1 | days | *start* |
| streak_floor | 1 | days | |
| gift_table | shells 60%, sea glass 30%, a pearl 10% | weights | *start* |

## Terms

| Term | Means |
| --- | --- |
| Tide gift | The one gift a player can claim each day |
| Reset | The moment a new tide gift can be claimed |
| Streak | Days in a row with a claim |

## Playtest hypotheses

Only for the first playable slice (claiming; the Streak is not in it).

1. If the tide gift waits on the beach at the first open of the day, then most players claim on that first open, measured by the share of days whose first beach visit ends in a claim. Held at 4 or more players of 6 on most days; Failed at 2 or fewer.
2. If `reset_time` is early in the morning, then few players meet a countdown on their first open, measured by first opens that land before the Reset. Held at no more than 1 player of 6; Failed at 2 or more.

## Dependencies

| Needs | From | Status |
| --- | --- | --- |
| A claim endpoint that checks the server clock | Engineering | Risk accepted: stubbed in the first build |
| Shell sprite and glow, three states | Art | Risk accepted: placeholder |

## Risks

- If the server is slow to answer a claim, then the one-tap moment feels broken. The claim shows at once and is rolled back if refused.

## Open questions

In `specs/open-questions.md`, rows `OQ-F001-*`.

## Approval

- Ready: Yes
- Approved by: Lead Designer
- Date: 2026-11-19
- Revision: rev-d2ee83c64152
- Commit: working copy
- Analysis: analysis-2026-11-19-02.md

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-11-19 | Ready (Lead Designer), against rev-d2ee83c64152; 1 advisory finding left open | Lead Designer |
| 2026-11-19 | `gift_table` parameter and its example row added (analysis run 01, finding 1) | Lead Designer |
| 2026-11-19 | OQ-F001-001 to 003 answered; F001.offline and the Offline state added (Clarify found the gap) | Lead Designer and Product Owner, applied by Agent |
| 2026-11-18 | First draft from the Product Owner's request | Lead Designer, applied by Agent |
