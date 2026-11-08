# F001: Daily tide gift

- Status: Draft
- Owner: Game Designer
- Last updated: 2026-11-08
- Links: none (fictional example)

## Intent

Give lapsed players a reason to open the game once a day, without punishing them for missing a day. Serves the pillar "Calm, never nagging".

## Player experience

The player opens the game and the tide has left something on the beach. Claiming it is one tap and feels like a small surprise. Missing a day should feel like nothing was lost, not like a broken streak.

## Today

Nothing. There is no daily reward.

## Scope

- In: one gift per day, a visible countdown to the next one, a streak that never resets to zero
- Out, for now: gift contents chosen by the player; push notifications
- Out, for good: paying to claim a missed day

## Job stories

1. When I open the game for the first time today, I want to collect what the tide left, so I can feel the game noticed I came back.
2. When I have already collected today's gift, I want to see when the next one arrives, so I can decide whether to come back tomorrow.

## Rules

### F001.claim-once: The gift can be claimed once per day

```gherkin
When      the player opens the beach screen
Provided  the player has not claimed a gift since the last reset
Then      the gift is shown on the beach and can be claimed
Otherwise the beach shows the time until the next reset
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| first open after the reset | yes | gift shown | |
| claimed 10 minutes ago | no | "Next tide in 13h 50m" | |
| claimed yesterday, opens today | yes | gift shown | |

### F001.streak-floor: A missed day lowers the streak by one, never to zero

```gherkin
When      the player claims a gift
Provided  the player claimed a gift in the previous day
Then      the streak goes up by one
Otherwise the streak goes down by one, to a minimum of ?
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| streak 4, claimed yesterday | yes | streak 5 | |
| streak 4, missed yesterday | no | streak 3 | |
| streak 1, missed three days | no | ? | minimum not decided: OQ-F001-001 |

## States

| State | What the player sees | How they get here | How they leave |
| --- | --- | --- | --- |
| Gift waiting | Shell on the beach, glowing | First open after reset | Taps the shell |
| Claimed | Reward card, then countdown | Taps the shell | Closes the card |
| Waiting | Countdown on the beach | Already claimed | Next reset |
| Offline | Shell greyed, "Tide is out" | No connection | Connection returns |

## Parameters

| Name | Value | Unit | Notes |
| --- | --- | --- | --- |
| reset_time | 05:00 | player's local time | early morning, so late players are not cut off at midnight |
| streak_floor | ? | days | OQ-F001-001 |

## Terms

| Term | Means |
| --- | --- |
| Reset | The moment a new gift becomes claimable, at `reset_time` |
| Streak | Days in a row with a claim, adjusted by F001.streak-floor |

## Playtest hypotheses

1. If missing a day only lowers the streak by one, then lapsed players will claim on return rather than ignore the beach, measured by claim rate on the first session after a gap.

## Risks

- If the player changes the device clock, then they can claim more than once a day. ? (OQ-F001-002)

## Open questions

See `specs/open-questions.md`, rows `OQ-F001-*`.

## Changelog

| Date | Change | By |
| --- | --- | --- |
| 2026-11-08 | First draft | Game Designer |
