"""Builds examples/tidepool-keeper/checkpoints/ for dl-prototype 0.3.

Run from the repo root: python3 tools/make_fixture.py .

Each checkpoint is a complete specs/ folder at one moment of the walkthrough.
Revisions in reports, approvals and tasks are computed, not typed.
"""
import shutil
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
sys.path.insert(0, str(REPO / "plugins/dl-prototype/scripts"))
import specdoc  # noqa: E402

OUT = REPO / "examples/tidepool-keeper/checkpoints"
FEAT = "features/F001-daily-tide-gift"

CONSTITUTION = """# Constitution: Tidepool Keeper

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
"""

GLOSSARY = """# Glossary

| Term (player-facing) | Code term | Means | Used in |
| --- | --- | --- | --- |
| Tide gift | daily_gift | The one gift a player can claim each day | F001 |
| Reset | daily_reset | The moment a new tide gift can be claimed, at `reset_time` in the player's local time, as the game server reckons it | F001 |
| Streak | streak | Days in a row with a claim, lowered but never zeroed by a missed day | F001 |
{extra}"""

REGISTER = """# Open questions

The single register for the project. Every `?` in a spec cites its question ID on the same line.

Blocking is against the current milestone (first playable): Yes, No, or `?` until triaged.

## Open

### F001: Daily tide gift

| ID | Question | Proposal | Owner | Blocking | Raised | Spec | Was |
| --- | --- | --- | --- | --- | --- | --- | --- |
{open_rows}

## Resolved

| ID | Question | Answer | Decided by | Date |
| --- | --- | --- | --- | --- |
{resolved_rows}

## Deferred

| ID | Question | Why deferred | Revisit at |
| --- | --- | --- | --- |
"""

Q1 = "| OQ-F001-001 | Lowest the streak can fall to: (a) 1, (b) half the best streak, (c) the last milestone | (a) 1 | Lead Designer | Yes | 2026-11-18 | F001.streak-floor | |"
Q2 = "| OQ-F001-002 | A player moves the phone clock forward a day: (a) the server decides the reset, claim needs a connection, (b) device time, risk accepted, (c) device time, with a server check on claim | (c) | Product Owner | Yes | 2026-11-18 | F001.claim-once | |"
Q3 = "| OQ-F001-003 | The player opens the beach with no connection: (a) show the gift and queue the claim, (b) grey the shell with \"Tide is out\" | (b), since a claim needs the server | Lead Designer | Yes | 2026-11-18 | F001 States | |"
Q4 = "| OQ-F001-004 | Does the countdown keep counting while the app is in the background? | Yes: it is worked out from `reset_time` on resume | Lead Designer | No | 2026-11-20 | F001.claim-once | |"
R1 = "| OQ-F001-001 | Lowest the streak can fall to | (a) 1 | Lead Designer | 2026-11-18 |"
R2 = "| OQ-F001-002 | Phone clock moved forward | (c) device time, with a server check on claim | Product Owner | 2026-11-19 |"
R3 = "| OQ-F001-003 | Opening the beach offline | (b) grey the shell, \"Tide is out\" | Lead Designer | 2026-11-18 |"

HEAD = """# F001: Daily tide gift

- Status: {status}
- Owner: Lead Designer
- Last updated: {date}
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
2. {story2}

## Rules

### F001.claim-once: The tide gift can be claimed once per day

```gherkin
When      the player opens the beach
Provided  the player has not claimed since the last Reset
Then      the tide gift is on the beach and one tap claims it
Otherwise {otherwise}
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| last claim yesterday at 09:00; opens today exactly at `reset_time` | yes | tide gift shown | the Reset has just passed |
| last claim yesterday at 09:00; opens today one minute before `reset_time` | no | {early} | the Reset is a minute away |
| claimed today at 09:00; opens today at 09:10 | no | {claimed} | already claimed since the Reset |
{gift_row}
### F001.server-time: The game server decides whether the Reset has passed

```gherkin
When      the player taps the tide gift
Provided  the game server agrees the last Reset is later than the player's last claim
Then      the claim is accepted and the gift goes into the pool
Otherwise the claim is refused and the beach shows the time to the next Reset, by the server's clock
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| claimed today at 09:00; sets the phone clock forward a day and taps | no | refused; countdown by the server's clock | {clock_why} |
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
| Streak 1, missed three days | no | Streak {floor_val} | {floor_why} |
{offline_rule}
## States

| State | What the player sees | How they get here | How they leave |
| --- | --- | --- | --- |
| Gift waiting | A shell on the beach, glowing | First open after the Reset | Taps the shell |
| Claimed | The gift card, then {after_claim} | Taps the shell | Closes the card |
| Waiting | {waiting} | Already claimed since the Reset | The next Reset |
{offline_state}
## Parameters

| Name | Value | Unit | Notes |
| --- | --- | --- | --- |
| reset_time | {reset} | player's local time | *start*; early, so late players are not cut off at midnight |
| streak_penalty | 1 | days | *start* |
| streak_floor | {floor_param} | days | |
{gift_param}
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

{approval}

## Changelog

| Date | Change | By |
| --- | --- | --- |
{changelog}"""

LAPSED = "- Ready: No (lapsed 2026-11-26: F001.claim-once changed; last approved {r9})\n- Approved by:\n- Date:\n- Revision:\n- Commit:\n- Analysis:"
NO_APPROVAL = "- Ready: No\n- Approved by:\n- Date:\n- Revision:\n- Commit:\n- Analysis:"

OFFLINE_RULE = """
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
"""
OFFLINE_STATE = "| Offline | The shell greyed, \"Tide is out\" | Opens the beach with no connection | The connection returns |\n"
GIFT_ROW = "| last claim yesterday; opens after the Reset | yes | tide gift shown, its contents drawn from `gift_table` | the gift's contents are a parameter |\n"
GIFT_PARAM = "| gift_table | shells 60%, sea glass 30%, a pearl 10% | weights | *start* |\n"


def spec(stage, approval=NO_APPROVAL, status="Draft", date="2026-11-18", reset="05:00", changelog=()):
    draft = stage == "draft"
    revised = stage == "revised"
    v = dict(
        status=status, date=date, reset=reset, approval=approval,
        story2=("When I have already collected today's gift, I want to see when the next one arrives, so I can decide whether to come back tomorrow."
                if not revised else "(dropped 2026-11-25: players did not use the countdown; see the playtest log, session 1)"),
        otherwise=("the beach shows the time until the next Reset" if not revised
                   else "the beach shows the empty shell, with no countdown"),
        early=("countdown \"Next tide in 1m\"" if not revised else "empty shell"),
        claimed=("countdown to the next `reset_time`" if not revised else "empty shell"),
        after_claim=("the time to the next tide" if not revised else "the empty shell"),
        waiting=("The empty shell, with the time to the next tide" if not revised else "The empty shell"),
        clock_why=("? the phone's clock or the server's (OQ-F001-002)" if draft else "the server's clock decides (OQ-F001-002)"),
        floor_val=("? (OQ-F001-001)" if draft else "1"),
        floor_why=("the floor is undecided" if draft else "never below `streak_floor`"),
        floor_param=("? (OQ-F001-001)" if draft else "1"),
        offline_rule=("" if stage in ("draft",) else OFFLINE_RULE),
        offline_state=("" if stage == "draft" else OFFLINE_STATE),
        gift_row=(GIFT_ROW if stage in ("reviewed", "approved", "revised") else ""),
        gift_param=(GIFT_PARAM if stage in ("reviewed", "approved", "revised") else ""),
        changelog="\n".join(changelog) + "\n",
    )
    if stage == "clarified":
        # Clarify found the offline gap: the rule exists, decided by OQ-F001-003
        pass
    return HEAD.format(**v)


def report(nn, rev, crev, grev, verdict, findings, resolutions="", focused=None, wording=()):
    lines = [f"# Analysis: F001 Daily tide gift (2026-11-{19 if nn == '01' else 19}, run {nn})", "",
             f"- Spec revision: {rev}",
             "- Spec commit: working copy",
             f"- Context: constitution {crev}, glossary {grev}",
             "- Inputs: spec.md; constitution.md; glossary.md; open-questions.md rows OQ-F001-*; no other feature specs exist yet",
             "- Access: the spec-analyst agent, Read only; inputs pasted by the lead; no shell, network or connectors",
             "- Run by a separate reviewer that saw only the inputs above, not code, tests, tickets, chats or earlier reports."]
    if focused:
        lines.append(f"- Focused rerun: {focused}")
    lines += ["", "## Verdict", "", verdict, "", "## Findings", "",
              "| # | Kind | Where | Finding | Evidence | Suggested fix | Severity |",
              "| --- | --- | --- | --- | --- | --- | --- |", *findings, "",
              "Wording notes:", "", *(wording or ["- None."]), "",
              "## Checked and found consistent", "",
              "Every rule has an Otherwise and examples on both sides. The times in F001.claim-once are written against `reset_time`, so they hold for any value. Terms match the glossary. The offline rule and state agree.",
              "", "## Other features this may affect", "", "| Feature | Why it may be affected | Checked |", "| --- | --- | --- |",
              "| None yet | F001 is the only feature | - |", "",
              "## Not checked", "", "- Feel, pacing, visual quality and fun, which are judged by playing.",
              "- Whether the build matches the spec (the build-checker's job).", "",
              "## Resolutions", "", "| # | Disposition | Reason | Decided by | Date |", "| --- | --- | --- | --- | --- |"]
    if resolutions:
        lines.append(resolutions)
    return "\n".join(lines) + "\n"


def rev_of(text):
    return specdoc.revision(text)


def write(cp, files):
    base = OUT / cp / "specs"
    for rel, text in files.items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    for d in ("features", "briefs", "overrides/templates"):
        (base / d).mkdir(parents=True, exist_ok=True)
        if not any((base / d).iterdir()):
            (base / d / ".gitkeep").write_text("")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    glossary = GLOSSARY.format(extra="")
    crev, grev = rev_of(CONSTITUTION), rev_of(glossary)
    state = lambda row: f"# STATE\n\n- Last updated: 2026-11-18 by Producer\n- Milestone: first playable: the daily tide gift on the beach\n\n## In flight\n\n| ID | What | Status | Next step |\n| --- | --- | --- | --- |\n{row}\n"
    base = {"constitution.md": CONSTITUTION, "glossary.md": glossary}

    # 01 start
    write("01-start", {**base, "STATE.md": state("| F001 | Daily tide gift | Not specced | Lead Designer: run spec |"),
                       "open-questions.md": REGISTER.format(open_rows="", resolved_rows="")})

    cl = ["| 2026-11-18 | First draft from the Product Owner's request | Lead Designer, applied by Agent |"]
    # 02 draft
    s = spec("draft", changelog=cl)
    write("02-draft", {**base, "STATE.md": state("| F001 | Daily tide gift | Draft | Lead Designer: run clarify |"),
                       "open-questions.md": REGISTER.format(open_rows="\n".join([Q2, Q1]), resolved_rows=""),
                       f"{FEAT}/spec.md": s})

    # 03 clarified: offline found, three answers in
    cl3 = ["| 2026-11-19 | OQ-F001-001 to 003 answered; F001.offline and the Offline state added (Clarify found the gap) | Lead Designer and Product Owner, applied by Agent |"] + cl
    s3 = spec("clarified", changelog=cl3, date="2026-11-19")
    reg3 = REGISTER.format(open_rows="", resolved_rows="\n".join([R2, R3, R1]))
    write("03-clarified", {**base, "STATE.md": state("| F001 | Daily tide gift | Draft | Agent: run analyze |"),
                           "open-questions.md": reg3, f"{FEAT}/spec.md": s3})

    # 04 analysed: one blocking finding
    r3 = rev_of(s3)
    rep1 = report("01", r3, crev, grev, "Findings to resolve: 1 blocking, 2 advisory", [
        "| 1 | Gap | F001.claim-once | Nothing says what the tide gift contains, so the claim cannot be built or tested | \"one tap claims it\" | Add a `gift_table` parameter and an example that uses it | Blocking |",
        "| 2 | Untestable | F001.server-time | The refused claim's countdown has no example with a time | \"countdown by the server's clock\" | Add the time in a later pass, or test it by the 09:10 row | Advisory |",
        "| 3 | Dependency | Dependencies | The claim endpoint is stubbed; the clock case cannot be proved until it exists | \"Risk accepted: stubbed\" | Keep the risk; mark the test case Blocked until then | Advisory |"],
        wording=["- Job story 2: \"collected\" and \"claimed\" both appear; the glossary uses claim."])
    write("04-analysed", {**base, "STATE.md": state("| F001 | Daily tide gift | Draft | Lead Designer: resolve finding 1 |"),
                          "open-questions.md": reg3, f"{FEAT}/spec.md": s3, f"{FEAT}/analysis-2026-11-19-01.md": rep1})

    # 05 reviewed: designer fixed finding 1 (new revision); focused rerun
    cl5 = ["| 2026-11-19 | `gift_table` parameter and its example row added (analysis run 01, finding 1) | Lead Designer |"] + cl3
    s5 = spec("reviewed", changelog=cl5, date="2026-11-19")
    r5 = rev_of(s5)
    rep1r = rep1.replace("| --- | --- | --- | --- | --- |\n", "| --- | --- | --- | --- | --- |\n", 1)
    rep1r = rep1r.rstrip("\n") + "\n| 1 | Fixed | `gift_table` added; checked in run 02 | Lead Designer | 2026-11-19 |\n| 2 | Open | Left for a later pass | Lead Designer | 2026-11-19 |\n| 3 | Open | Risk accepted | Producer | 2026-11-19 |\n"
    rep2 = report("02", r5, crev, grev, "Findings to resolve: 0 blocking, 1 advisory", [
        "| 1 | Untestable | F001.server-time | Carried from run 01, finding 2: the refused claim's countdown has no example with a time | \"countdown by the server's clock\" | As before | Advisory |"],
        focused="the edited rule F001.claim-once and the Parameters table, plus run 01's findings 1 and 2")
    files5 = {**base, "STATE.md": state("| F001 | Daily tide gift | Draft | Lead Designer: approve as Ready |"),
              "open-questions.md": reg3, f"{FEAT}/spec.md": s5,
              f"{FEAT}/analysis-2026-11-19-01.md": rep1r, f"{FEAT}/analysis-2026-11-19-02.md": rep2}
    write("05-reviewed", files5)

    # 06 approved
    appr = (f"- Ready: Yes\n- Approved by: Lead Designer\n- Date: 2026-11-19\n- Revision: {r5}\n"
            "- Commit: working copy\n- Analysis: analysis-2026-11-19-02.md")
    cl6 = [f"| 2026-11-19 | Ready (Lead Designer), against {r5}; 1 advisory finding left open | Lead Designer |"] + cl5
    s6 = spec("approved", approval=appr, status="Ready", changelog=cl6, date="2026-11-19")
    assert rev_of(s6) == r5, "approval must not change the revision"
    files6 = {**files5, "STATE.md": state("| F001 | Daily tide gift | Ready | Agent: run tasks |"), f"{FEAT}/spec.md": s6}
    write("06-approved", files6)

    # 07 ticketed
    tasks = TASKS.format(rev=r5, status=f"Ready, approved by Lead Designer on 2026-11-19 against {r5}")
    files7 = {**files6, "STATE.md": state("| F001 | Daily tide gift | Building | Agent: build S1 (brief B001) |"),
              f"{FEAT}/tasks.md": tasks, f"{FEAT}/test-plan.md": PLAN.format(rev=r5, runs="", status_a="Not run", status_b="Not run", status_c="Not run", status_d="Not run", status_e="Blocked: claim endpoint stubbed", expect_c="countdown to the next `reset_time`", expect_b="countdown \"Next tide in 1m\"", build=""),
              f"{FEAT}/test-room.md": ROOM.format(rev=r5), f"{FEAT}/summary.md": SUMMARY.format(rev=r5)}
    write("07-ticketed", files7)

    # 08 proved
    reg8 = REGISTER.format(open_rows=Q4, resolved_rows="\n".join([R2, R3, R1]))
    runs = "| 2026-11-21 | build 0.1.7 | QA Lead | 5 | 4 | 0 | 1 | TC-F001.server-time-01 blocked: endpoint stubbed |"
    plan8 = PLAN.format(rev=r5, runs=runs, status_a="Pass", status_b="Pass", status_c="Pass", status_d="Pass", status_e="Blocked: claim endpoint stubbed", expect_c="countdown to the next `reset_time`", expect_b="countdown \"Next tide in 1m\"", build="0.1.7")
    files8 = {**files7, "STATE.md": state("| F001 | Daily tide gift | Building | QA Lead: run the playtest |"),
              "open-questions.md": reg8, f"{FEAT}/test-plan.md": plan8, "briefs/B001-claim-endpoint-stub.md": BRIEF}
    write("08-proved", files8)

    # 09 tuned: reset_time 05:00 -> 04:00, approval carried over (Parameters only)
    r9 = rev_of(spec("approved", status="Ready", changelog=cl6, date="2026-11-25", reset="04:00"))
    appr9 = (f"- Ready: Yes\n- Approved by: Lead Designer\n- Date: 2026-11-25\n- Revision: {r9}\n"
             "- Commit: working copy\n- Analysis: analysis-2026-11-19-02.md\n"
             f"- Carried over: from {r5}, tuning only (reset_time 05:00 to 04:00)")
    cl9 = [f"| 2026-11-25 | `reset_time` 05:00 to 04:00 (playtest session 1, hypothesis 2 Failed). Tuning only: approval carried over from {r5}; S1's scenarios name `reset_time`, not a clock time, so they stand; the three cases that set the clock by `reset_time` to be rerun | Lead Designer, applied by Agent |"] + cl6
    s9 = spec("approved", approval=appr9, status="Ready", changelog=cl9, date="2026-11-25", reset="04:00")
    assert rev_of(s9) == r9
    log9 = PLAYTEST_LOG
    plan9 = PLAN.format(rev=r9, runs=runs, status_a="Rerun: reset_time now 04:00", status_b="Rerun: reset_time now 04:00", status_c="Rerun: reset_time now 04:00", status_d="Pass", status_e="Blocked: claim endpoint stubbed", expect_c="countdown to the next `reset_time`", expect_b="countdown \"Next tide in 1m\"", build="0.1.7")
    tasks9 = tasks.replace(f"against {r5}", f"against {r9} (carried over from {r5}, tuning only)").replace(f"Built from: spec revision {r5}", f"Built from: spec revision {r9} (carried over from {r5}, tuning only)")
    files9 = {**files8, "STATE.md": state("| F001 | Daily tide gift | Building | QA Lead: rerun the three reset_time cases on build 0.1.8 |"),
              f"{FEAT}/spec.md": s9, f"{FEAT}/playtest-log.md": log9,
              f"{FEAT}/summary.md": SUMMARY.format(rev=r9).replace("2026-11-19, against", "2026-11-25, against").replace("at 05:00", "at 04:00"), f"{FEAT}/test-plan.md": plan9, f"{FEAT}/tasks.md": tasks9}
    write("09-tuned", files9)

    # 10 revised: job story 2 dropped and the Otherwise changed: approval lapses
    cl10 = ["| 2026-11-26 | Job story 2 dropped; F001.claim-once's Otherwise shows the empty shell, no countdown (playtest session 1: nobody used the countdown). Rule change: approval lapsed; story S1 to Recheck; three test cases Stale | Lead Designer, applied by Agent |"] + cl9
    s10 = spec("revised", approval=LAPSED.format(r9=r9), status="Draft", changelog=cl10, date="2026-11-26", reset="04:00")
    tasks10 = tasks9.replace(f"**Status:** Ready, approved by Lead Designer on 2026-11-19 against {r9} (carried over from {r5}, tuning only)", "**Status:** Recheck: F001.claim-once (changed 2026-11-26). Built work and its test record are kept.")
    plan10 = PLAN.format(rev=r9, runs=runs, status_a="Stale: F001.claim-once changed", status_b="Stale: F001.claim-once changed", status_c="Stale: F001.claim-once changed", status_d="Pass", status_e="Blocked: claim endpoint stubbed", expect_c="empty shell", expect_b="empty shell", build="0.1.7")
    files10 = {**files9, "STATE.md": state("| F001 | Daily tide gift | Draft (rule change after playtest) | Agent: run analyze on the new revision |"),
               f"{FEAT}/spec.md": s10, f"{FEAT}/tasks.md": tasks10, f"{FEAT}/test-plan.md": plan10}
    write("10-revised", files10)
    print("revisions:", {"03": r3, "05": r5, "09": r9, "10": rev_of(s10)})


TASKS = """# F001: Daily tide gift, tasks

- Built from: spec revision {rev}, approved by Lead Designer on 2026-11-19 (working copy)
- Ticket system: local, `tasks.md` only (this example posts nothing)
- Slice: claiming the tide gift on the beach, online and offline, with the server's clock. The Streak (F001.streak-floor) is not ticketed.

## Story S1: Claim the tide gift

**Status:** {status}

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
"""

PLAN = """# F001: Daily tide gift, test plan

- Owner: QA Lead
- Written from: spec revision {rev} (story S1 in `tasks.md`)
- Test room: `test-room.md`
- Last run: build {build}

## Cases

| Case | Rule | Example row | Set-up (room, spawn, state) | Do | Expect | Kind | Status | Build | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-F001.claim-once-01 | F001.claim-once | opens exactly at `reset_time` | spawn a; last claim yesterday 09:00; clock set to `reset_time` | open the beach | tide gift shown | Boundary | {status_a} | {build} | |
| TC-F001.claim-once-02 | F001.claim-once | opens one minute before `reset_time` | spawn a; last claim yesterday 09:00; clock one minute before `reset_time` | open the beach | {expect_b} | Boundary | {status_b} | {build} | |
| TC-F001.claim-once-03 | F001.claim-once | claimed at 09:00, opens at 09:10 | spawn a; claimed today 09:00 | open the beach at 09:10 | {expect_c} | Guard | {status_c} | {build} | |
| TC-F001.offline-01 | F001.offline | no connection, not claimed | spawn a; network off (debug key N) | open the beach | greyed shell, "Tide is out" | Error | {status_d} | {build} | |
| TC-F001.server-time-01 | F001.server-time | phone clock forward a day | spawn a; claimed today; debug key C moves the phone clock | tap the shell | refused; server countdown | Guard | {status_e} | {build} | |

## Not covered by this plan

- F001.streak-floor: not in the slice.
- Whether claiming feels like a small surprise: the playtest's job.

## Run log

| Date | Build | Who | Cases run | Pass | Fail | Blocked | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
{runs}
"""

ROOM = """# F001 test room

- Status: Approved by Lead Designer 2026-11-19
- For: `tasks.md` story S1; every case in `test-plan.md`
- Spec: revision {rev}
- Built by: a scene script, `Scenes/F001TestBeach`

One beach screen with the shell spot and a debug panel.

```
+--------------------------------+
|                      [debug]   |
|                                |
|        (shell)                 |
|   a                            |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
+--------------------------------+
```

## Spawns and markers

| Marker | Position | Used by cases | Why it is here |
| --- | --- | --- | --- |
| a | left of the shell | all five | the player starts in view of the shell |

## Controls for testing

- Debug key T: set the game clock (and the server stub's clock) to any time.
- Debug key C: move only the phone's clock forward a day.
- Debug key N: drop or restore the connection.
"""

SUMMARY = """# Daily tide gift, in plain words

- Feature: F001 ([spec](spec.md))
- Status: Ready
- Written: 2026-11-19, against spec revision {rev}, for readers outside the team. The spec is the source of truth.

## What the feature does

- **One gift a day.** Once a day the tide leaves a gift on the beach. One tap collects it.
- **A new one each morning.** The next gift arrives at 05:00 in the player's own time, so late players are not cut off at midnight.
- **No cheating the clock.** The game server decides when a new day has started, so moving the phone's clock does not give a second gift.
- **Offline is calm.** With no connection the shell is greyed with "Tide is out" until the connection returns.
- **Missing a day costs little.** The streak drops by one, never to zero. (Not in the first build.)

## What is left out, for now

- Choosing your gift; reminders.

## Questions waiting on you

- None.
"""

BRIEF = """# B001: Stub the claim endpoint (2026-11-20)

- Owner: one fresh engineering helper. Stop when done.
- Spec: F001, revision as in `tasks.md`; story S1.T3

## Context (all of it)

Read `specs/constitution.md`, `specs/STATE.md` and `specs/features/F001-daily-tide-gift/spec.md` first. The real claim endpoint is not built; the dependency is accepted as a risk.

## What to build

1. A stub that answers a claim with accepted or refused from its own clock, which debug key T sets.
2. The beach states Gift waiting, Claimed, Waiting and Offline, from F001's States table.
3. Prove it: run the build on the Android emulator, claim once, press C, reopen online and offline. Report what the beach showed each time.

## Rules

- Every value comes from Parameters; nothing hard-coded.

## Not in this brief

- The Streak.

## Report back

Built and proved on build 0.1.7. Claim, offline and the already-claimed countdown behave as the spec says. Pressing C showed a second gift at first: the stub read the phone's clock. Fixed in the same brief and proved again. One gap raised, not guessed: does the countdown keep counting in the background (OQ-F001-004, not blocking).
"""

PLAYTEST_LOG = """# F001: Daily tide gift, playtest log

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
"""


if __name__ == "__main__":
    main()
