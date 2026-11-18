# F001: Daily tide gift, tasks

- Built from: spec revision rev-d2ee83c64152, approved by Lead Designer on 2026-11-19 (working copy)
- Ticket system: local, `tasks.md` only (this example posts nothing)
- Slice: claiming the tide gift on the beach, online and offline, with the server's clock. The Streak (F001.streak-floor) is not ticketed.

## Story S1: Claim the tide gift

**Status:** Ready, approved by Lead Designer on 2026-11-19 against rev-d2ee83c64152

**Job story:** When I open the game for the first time today, I want to collect what the tide left, so I can feel the game noticed I came back.

**Spec rules:** F001.claim-once, F001.server-time, F001.offline

**Acceptance criteria** (each scenario names the rule and example row it comes from; times are written against `reset_time`)

```gherkin
Scenario: Gift waiting exactly at the Reset (F001.claim-once, row 1)
  Given the player last claimed yesterday after the Reset
  When  they open the beach at exactly reset_time today, online
  Then  the tide gift is on the beach and one tap claims it

Scenario: Already claimed today (F001.claim-once, row 3: guard)
  Given the player claimed today after the Reset
  When  they open the beach ten minutes later
  Then  no gift is shown, and the beach shows the time to the next Reset

Scenario: Phone clock moved forward (F001.server-time, row 1: guard)
  Given the player claimed today after the Reset
  When  they set the phone clock forward a day and tap
  Then  the claim is refused and the countdown follows the server's clock

Scenario: No connection (F001.offline, row 2: error)
  Given the player has not claimed since the Reset
  When  they open the beach with no connection
  Then  the shell is greyed with "Tide is out" and cannot be tapped
```

**Tasks**

| ID | Discipline | Task | Depends on |
| --- | --- | --- | --- |
| S1.T1 | Design | Approve the test room (`test-room.md`) | |
| S1.T2 | Art | Shell sprite and glow, three states (placeholder accepted) | |
| S1.T3 | Engineering | Beach states and the claim, with a stubbed endpoint (brief B001) | S1.T1 |
| S1.T4 | QA | Run `test-plan.md` on the emulator | S1.T3 |

**Proved by:** QA runs the test plan on the Android emulator; the Lead Designer claims once on a phone.

## Universal Ready check

| Point | S1 |
| --- | --- |
| 1. Title follows the naming convention | Yes |
| 2. Links to its spec and revision | Yes |
| 3. At least three acceptance points, what not how | Yes (4) |
| 4. Parent story linked (tasks) | Yes |
| 5. Dependencies done or accepted as a risk | Risk accepted: endpoint stubbed, art placeholder |

## Not ticketed

- F001.streak-floor: the Streak waits for a second slice.
