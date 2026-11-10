# Design-led SDD: Worked example

One feature, F001 Daily tide gift, taken once round the whole prototype loop. Tidepool Keeper is a fictional cosy mobile game whose first design pillar is "Calm, never nagging". Every name, number and playtest result below is invented to show the method; none comes from a real project. The spec as it stood after step 2 is in [`examples/tidepool-keeper`](../examples/tidepool-keeper/specs/features/F001-daily-tide-gift/spec.md).

## Step 1. Request

The product owner sends one line: *"Players should get something for coming back each day, but I don't want it to feel like a chore."*

The designer runs `/dl-prototype:spec`. The skill reads the constitution and glossary first, then checks the size: this is a new system other disciplines build on, so it takes the full path, not a brief. It checks the request against the pillars ("never nagging" rules out a streak that resets to zero) and creates `specs/features/F001-daily-tide-gift/spec.md`.

It asks the designer one question at a time, for example:

> **When should a new gift become available?** (a) 05:00 in the player's local time (recommended: late players are not cut off at midnight), (b) midnight local time, (c) 24 hours after the last claim.

The designer picks (a). Questions only the owner can answer are not asked here; they become `?` places.

## Step 2. Spec draft

The first draft is Status: Draft, with two `?` places the builders could not proceed without.

**Intent.** Give lapsed players a reason to open the game once a day without punishing them for missing one.

**Scope.** In: one gift per day, a visible countdown, a streak that never resets to zero. Out for now: player-chosen gifts, push notifications. Out for good: paying to claim a missed day.

**Job stories**

1. When I open the game for the first time today, I want to collect what the tide left, so I can feel the game noticed I came back.
2. When I have already collected today's gift, I want to see when the next one arrives, so I can decide whether to come back tomorrow.

**Rules**

```gherkin
Rule F001.claim-once: The gift can be claimed once per day
  When      the player opens the beach screen
  Provided  the player has not claimed since the last reset
  Then      the gift is shown and can be claimed
  Otherwise the beach shows the time until the next reset

Rule F001.streak-floor: A missed day lowers the streak by one, never to zero
  When      the player claims a gift
  Provided  the player claimed in the previous day
  Then      the streak goes up by one
  Otherwise the streak goes down by one, to a minimum of ?
```

| Rule | Situation | Provided | Outcome |
| --- | --- | --- | --- |
| claim-once | first open after the reset | yes | gift shown |
| claim-once | claimed 10 minutes ago | no | "Next tide in 13h 50m" |
| streak-floor | streak 4, claimed yesterday | yes | streak 5 |
| streak-floor | streak 4, missed yesterday | no | streak 3 |
| streak-floor | streak 1, missed three days | no | ? |

**Parameters.** `reset_time` = 05:00 player's local time. `streak_floor` = ?.

**Risk.** If the player changes the device clock, then they can claim more than once a day. ?

## Step 3. Clarify

`/dl-prototype:clarify` lists the two marked `?` places, then checks the gap list and finds one more nobody had marked: what happens if the player is offline when they open the beach.

| ID | Question | Owner | Blocking | Answer |
| --- | --- | --- | --- | --- |
| OQ-F001-001 | Lowest the streak can fall to: (a) 1, (b) half the best streak, (c) the last milestone | Game Designer | Yes | (a) 1. Simplest to read; revisit after playtest |
| OQ-F001-002 | Clock changes: (a) server time decides the reset, (b) device time, risk accepted, (c) device time with a server check on claim | Product Owner | Yes | (c). Works offline; cheaters gain at most one gift |
| OQ-F001-003 | Offline on open: (a) show the gift, queue the claim, (b) grey the shell with "Tide is out" | Game Designer | Yes | (b). Matches (c) above: a claim needs the server |

The designer answers 001 and 003 on the spot, one multiple-choice question each. 002 is a business question about cheating risk, so clarify drafts a note for the product owner instead of answering it:

> A player sets their phone clock forward a day and opens the game. Should they get a second gift? (a) No, the server decides; the game needs a connection to claim. (b) Yes, we accept it. (c) Only if the server agrees when they claim; offline players wait.

The owner picks (c). Each answer is written into the spec, the `?` removed, and the register row moved to Resolved with who decided. No blocking question is left.

## Step 4. Analyse

`/dl-prototype:analyze` starts a fresh checking agent that reads only the spec, constitution, glossary and register: no code, tickets or chat. It returns three findings, written to `analysis-2026-11-09.md`.

| # | Kind | Where | Finding | Resolution |
| --- | --- | --- | --- | --- |
| 1 | Gap | F001.claim-once | Examples cover only one claim per day; nothing says what the reward is | Designer adds a `gift_table` parameter and a third example |
| 2 | Value inside rule | F001.streak-floor | "down by one" puts a tuning value in the rule text | Moved to parameter `streak_penalty` = 1 |
| 3 | State missing | States table | Offline state from OQ-F001-003 is reachable but not listed | Added "Offline: shell greyed, Tide is out" |

All three are resolved by edits, and the designer marks the spec **Ready**. The report also says what it could not judge: whether the claim moment feels like a small surprise. That is left to the playtest.

## Step 5. Tasks

`/dl-prototype:tasks` asks which slice to ticket and recommends the smallest playable one: claiming the gift, without the streak. It writes `tasks.md` with one story.

**Story S1: Claim the daily tide gift.** When I open the game for the first time today, I want to collect what the tide left, so I can feel the game noticed I came back. Implements F001.claim-once.

```gherkin
Scenario: Gift waiting after the reset
  Given the player last claimed before today's 05:00 reset
  When  they open the beach screen while online
  Then  the shell glows and one tap claims the gift

Scenario: Already claimed today (guard)
  Given the player claimed at 09:00 today
  When  they open the beach screen at 09:10
  Then  the beach shows "Next tide in 19h 50m" and no shell

Scenario: Offline on open (error)
  Given the player has not claimed today
  When  they open the beach screen with no connection
  Then  the shell is greyed with "Tide is out" and cannot be tapped
```

| ID | Discipline | Task | Depends on |
| --- | --- | --- | --- |
| S1.T1 | Design | Shell states: waiting, claimed, offline | |
| S1.T2 | Art | Shell sprite and glow, three states | S1.T1 |
| S1.T3 | Engineering | Claim with server check; countdown from `reset_time` | S1.T2 |
| S1.T4 | QA | Pass or fail per scenario, on Android and iOS | S1.T3 |

**Proved by:** the designer claims on a phone, changes the device clock, and confirms no second gift. **Not ticketed:** the streak, left for the next slice.

## Step 6. Build and prove

The lead agent writes one brief per engineering task and hands each to a single helper, never two on the same files. The engineering brief, B001, ends with its proof step:

> **Prove it:** run the build on the Android emulator, claim once, set the device clock forward a day, reopen online and offline. Report what the beach showed each time.

The helper reports back in under ten lines: claim works, offline greys the shell, but the clock test shows a second gift. The server check was reading device time. That is a defect, not a spec gap, so it is fixed in the same brief and proved again.

The helper also reports one real gap: the spec never says whether the countdown keeps ticking while the app is in the background. The lead raises **OQ-F001-004** instead of guessing, and the designer answers it (yes, it is computed from `reset_time` on resume).

## Step 7. Playtest

Six internal players use the build for a week; the producer collects notes. `/dl-prototype:playtest` separates what players did from what they said, then writes Session 1 at the top of `playtest-log.md`.

**What we saw (observations)**

- Four of six players claimed on the first open of each day.
- Two players opened the beach before 05:00 on most days and saw only a countdown.
- No player opened the beach twice in one day to check the countdown.

**Hypotheses**

| # | Hypothesis | Result | Evidence |
| --- | --- | --- | --- |
| 1 | A gift on first open brings lapsed players back to the beach | Unclear | Too few lapsed days in one week |
| 2 | Players use the countdown to plan their return | Failed | Nobody rechecked the countdown |

**Proposed spec changes**, each accepted by the designer one at a time:

| Spec part | Change | Kind | Accepted |
| --- | --- | --- | --- |
| Parameter `reset_time` | 05:00 to 04:00 | Tuning | Yes, applied directly |
| Job story 2 | Dropped; countdown kept as a small label only | Scope | Yes, `analyze` rerun |
| Pillar "never nagging" | One player wanted a reminder; challenges the pillar | Pillar | Flagged to the designer, no change |

The graduation check runs last. The feature gives out currency, but the last session still changed scope, so it stays in the prototype tier for now.

## What changed in the spec

The spec's own changelog after one loop, newest first.

| Step | Change | Source |
| --- | --- | --- |
| 7. Playtest | `reset_time` 05:00 to 04:00; job story 2 dropped | Session 1: early openers, countdown unused |
| 6. Build | Countdown computed from `reset_time` on resume | OQ-F001-004, raised by the helper |
| 4. Analyse | `gift_table` and `streak_penalty` parameters; Offline state added | Analysis findings 1 to 3 |
| 3. Clarify | Streak floor 1; server check on claim; offline greys the shell | OQ-F001-001 to 003 |
| 2. Spec | First draft with two `?` places | Owner's request |

Nothing in the spec changed without a row here, and no row lacks its reason.
