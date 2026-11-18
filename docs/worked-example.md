# Design-led SDD: Worked example

One feature, F001 Daily tide gift, taken once round the whole prototype loop. Tidepool Keeper is a fictional cosy mobile game whose first design pillar is "Calm, never nagging". Every name, number and playtest result below is invented to show the method; none comes from a real project.

Every step has a matching folder in [`examples/tidepool-keeper/checkpoints`](../examples/tidepool-keeper/README.md): the whole `specs/` folder as it stood at that moment. You can open any of them and run the Ready check on it. The checkpoint for each step is named in its heading.

The team's titles are set in the constitution's Roles table: the Lead Designer is the method's designer, the Product Owner is the owner, and the QA Lead is QA.

## Step 1. Request (checkpoint 01-start)

The Product Owner sends one line: *"Players should get something for coming back each day, but I don't want it to feel like a chore."*

The Lead Designer runs `/dl-prototype:spec`. The skill reads the constitution and glossary first, then checks the size: this is a new system other disciplines build on, so it takes the full path, not a brief. It checks the request against the pillars ("never nagging" rules out a streak that resets to zero) and creates `specs/features/F001-daily-tide-gift/spec.md`.

It asks the designer one question at a time, for example:

> **When should a new gift become available?** (a) 05:00 in the player's local time (recommended: late players are not cut off at midnight), (b) midnight local time, (c) 24 hours after the last claim.

The designer picks (a). It becomes the parameter `reset_time`. Questions only the owner can answer are not asked here; they become `?` places.

## Step 2. Spec draft (checkpoint 02-draft)

The first draft is Status: Draft, with two `?` places. Each cites its question in the register on the same line, so nobody has to guess what it waits on.

**Rules** (each has a When, a Provided, a Then and an Otherwise, and an examples table with both sides of the guard)

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

The times are written against `reset_time`, not as clock times. That matters later: when playtesting moves the reset, these rows still hold.

The other rules are F001.server-time (the server decides whether the Reset has passed: undecided, waiting on OQ-F001-002) and F001.streak-floor (how low the streak can fall: undecided, waiting on OQ-F001-001).

The Ready check fails, and says why in plain lines:

```
Ready check (approve): FAIL
  FAIL  OQ-F001-002 is open and blocking
  FAIL  OQ-F001-001 is open and blocking
  FAIL  line 59 is undecided and waits on OQ-F001-002
  ...
  FAIL  no analysis report: run analyze on this revision
```

## Step 3. Clarify (checkpoint 03-clarified)

`/dl-prototype:clarify` lists the two marked `?` places, then checks the gap list and finds one nobody had marked: what happens if the player is offline when they open the beach. The QA Lead, who joins at Clarify, asks the same thing from the other side: "How would I test the claim with the network off?"

| ID | Question | Proposal | Owner | Answer |
| --- | --- | --- | --- | --- |
| OQ-F001-001 | Lowest the streak can fall to: (a) 1, (b) half the best streak, (c) the last milestone | (a) | Lead Designer | (a) 1 |
| OQ-F001-002 | Phone clock moved forward a day: (a) the server decides, (b) device time, risk accepted, (c) device time, with a server check on claim | (c) | Product Owner | (c) |
| OQ-F001-003 | Opening the beach offline: (a) show the gift and queue the claim, (b) grey the shell with "Tide is out" | (b) | Lead Designer | (b) |

The designer answers 001 and 003, one multiple-choice question each. 002 is a business question about cheating risk, so clarify drafts a note for the Product Owner instead of answering it. Each answer goes into the spec; 003 becomes a new rule, F001.offline, and an Offline state. The register rows move to Resolved, with who decided.

No `?` is left, but the check still fails: nobody independent has read this revision yet.

## Step 4. Analyse (checkpoint 04-analysed)

`/dl-prototype:analyze` hands the spec, constitution, glossary and the feature's register rows to the plugin's `spec-analyst` agent. It can only read what it is given: no code, tickets, chats or earlier reports. Its report, `analysis-2026-11-19-01.md`, records which revision it read (`rev-8a70386003e4`), the context it read, and what access the reviewer had.

| # | Kind | Where | Finding | Severity |
| --- | --- | --- | --- | --- |
| 1 | Gap | F001.claim-once | Nothing says what the tide gift contains, so the claim cannot be built or tested | Blocking |
| 2 | Untestable | F001.server-time | The refused claim's countdown has no example with a time | Advisory |
| 3 | Dependency | Dependencies | The claim endpoint is stubbed, so the clock case cannot be proved until it exists | Advisory |

The report also says what it could not judge: whether the claim feels like a small surprise. That is left to the playtest.

## Step 5. Fix and recheck (checkpoint 05-reviewed)

The designer adds a `gift_table` parameter and an example that uses it. That edit changes the spec's revision (now `rev-d2ee83c64152`), so the first report no longer counts. Marking finding 1 "Fixed" in that report is not enough: the check asks for a report on the edited spec.

A focused rerun, `analysis-2026-11-19-02.md`, rechecks the edited rule, the Parameters table and the earlier findings. It finds no blocking problems; the advisory finding is carried and left open, which is allowed. The approve-stage check now passes. The ticket stage still fails: nobody has said yes.

## Step 6. Approve the spec (checkpoint 06-approved)

Clarify asks the designer: "Mark F001 Ready against `rev-d2ee83c64152`, with one advisory finding left open?" The designer says yes. Only then does the agent fill the Approval section:

```
- Ready: Yes
- Approved by: Lead Designer
- Date: 2026-11-19
- Revision: rev-d2ee83c64152
- Commit: working copy
- Analysis: analysis-2026-11-19-02.md
```

Recording the approval does not change the revision: the Approval, Changelog, Status and date lines are left out of it on purpose.

## Step 7. Tasks, test plan and test room (checkpoint 07-ticketed)

`/dl-prototype:tasks` runs the ticket-stage check first, then asks which slice to ticket and recommends the smallest playable one: claiming the gift, without the streak. It writes `tasks.md` with one story, S1, written as Draft. Each scenario names the rule and example row it comes from:

```gherkin
Scenario: Already claimed today (F001.claim-once, row 3: guard)
  Given the player claimed today after the Reset
  When  they open the beach ten minutes later
  Then  no gift is shown, and the beach shows the time to the next Reset
```

In the same step, QA is brought in early:

- **`test-plan.md`**: one case per example row in the slice, five in all, such as `TC-F001.claim-once-03` (Guard) and `TC-F001.offline-01` (Error). The server-time case is already marked Blocked, because the endpoint is stubbed.
- **`test-room.md`**: one greybox beach with a spawn and debug keys to set the clock (T), move only the phone's clock (C) and drop the network (N). The designer approves it before S1 is built.
- **`summary.md`**: the feature in plain words, for a new tester or the Product Owner. A tester can start here with no briefing.

The designer approves S1 as its own step. Its Status line now reads "Ready, approved by Lead Designer on 2026-11-19 against rev-d2ee83c64152", and the story-stage check passes. Tickets stay in `tasks.md` in this example.

## Step 8. Build and prove (checkpoint 08-proved)

The lead agent writes brief B001 and hands it to a single helper. It ends with its proof step: run the build on the Android emulator, claim once, press C, reopen online and offline, and report what the beach showed.

The helper reports back: the clock test showed a second gift. The stub was reading the phone's clock. That is a defect, not a spec gap, so it is fixed in the same brief and proved again. The helper also reports one real gap: does the countdown keep counting while the app is in the background? The lead raises **OQ-F001-004** (not blocking) instead of guessing.

The QA Lead runs the test plan on build 0.1.7: five cases run, four pass, one blocked by the stub. The plugin's `build-checker` agent can do the same mapping on the code side, rule by rule, without changing anything.

## Step 9. Playtest and tuning (checkpoint 09-tuned)

The hypotheses in the spec cover only what was built. There is no streak hypothesis, because the streak was not in the build. Each has its Held and Failed lines written down before anyone plays:

| # | Hypothesis | Held if | Failed if | Result |
| --- | --- | --- | --- | --- |
| 1 | Players claim on their first visit to the beach each day | 4 or more of 6, on most days | 2 or fewer | Held |
| 2 | Few players meet a countdown on their first open | no more than 1 of 6 | 2 or more | Failed |

Two players opened the beach before 05:00 on most days. The designer moves `reset_time` to 04:00. `spec_diff.py` confirms the kind of change:

```
Change: tuning (rev-d2ee83c64152 to rev-7a9c2eb43fb2)
Sections changed: Parameters
Parameters changed: reset_time
```

Because only a parameter changed, and S1's scenarios name `reset_time` rather than a clock time, the designer carries the approval over instead of rerunning analysis. The Approval section gets the new revision and one more line:

```
- Carried over: from rev-d2ee83c64152, tuning only (reset_time 05:00 to 04:00)
```

The three test cases that set the clock by `reset_time` are marked to be rerun on the next build. All three stages of the Ready check still pass.

## Step 10. A rule change (checkpoint 10-revised)

The playtest also showed that no player went back to check the countdown. The designer drops job story 2 and changes F001.claim-once's Otherwise: the beach now shows the empty shell, with no countdown. That is a rule change, not tuning:

```
Change: rule (rev-7a9c2eb43fb2 to rev-681876b2e441)
Rules changed: F001.claim-once
Story S1 (...): F001.claim-once
Case TC-F001.claim-once-01: F001.claim-once
Case TC-F001.claim-once-02: F001.claim-once
Case TC-F001.claim-once-03: F001.claim-once
```

So the approval lapses. The spec goes back to Draft, S1 is marked `Recheck: F001.claim-once`, and the three cases are marked Stale. Nothing is deleted: the built work and its test record stay. The offline case is untouched, because F001.offline did not change. The next move is analyze on the new revision, then the designer's yes, then the story again.

## What changed in the spec

The spec's own changelog after one loop, newest first.

| Step | Change | Effect on approval |
| --- | --- | --- |
| 10 | Job story 2 dropped; F001.claim-once shows the empty shell | Lapsed; S1 to Recheck; three cases Stale |
| 9 | `reset_time` 05:00 to 04:00 | Carried over as tuning |
| 6 | Ready (Lead Designer), against `rev-d2ee83c64152` | Approved |
| 5 | `gift_table` added (analysis run 01, finding 1) | New revision; focused rerun |
| 3 | Questions 001 to 003 answered; F001.offline added | |
| 2 | First draft | |

Nothing in the spec changed without a row here, and no row lacks its reason.
