# F001: Daily tide gift, test plan

- Owner: QA Lead
- Written from: spec revision rev-d2ee83c64152 (story S1 in `tasks.md`)
- Test room: `test-room.md`
- Last run: build 0.1.7

## Cases

| Case | Rule | Example row | Set-up (room, spawn, state) | Do | Expect | Kind | Status | Build | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-F001.claim-once-01 | F001.claim-once | opens exactly at `reset_time` | spawn a; last claim yesterday 09:00; clock set to `reset_time` | open the beach | tide gift shown | Boundary | Pass | 0.1.7 | |
| TC-F001.claim-once-02 | F001.claim-once | opens one minute before `reset_time` | spawn a; last claim yesterday 09:00; clock one minute before `reset_time` | open the beach | countdown "Next tide in 1m" | Boundary | Pass | 0.1.7 | |
| TC-F001.claim-once-03 | F001.claim-once | claimed at 09:00, opens at 09:10 | spawn a; claimed today 09:00 | open the beach at 09:10 | countdown to the next `reset_time` | Guard | Pass | 0.1.7 | |
| TC-F001.offline-01 | F001.offline | no connection, not claimed | spawn a; network off (debug key N) | open the beach | greyed shell, "Tide is out" | Error | Pass | 0.1.7 | |
| TC-F001.server-time-01 | F001.server-time | phone clock forward a day | spawn a; claimed today; debug key C moves the phone clock | tap the shell | refused; server countdown | Guard | Blocked: claim endpoint stubbed | 0.1.7 | |

## Not covered by this plan

- F001.streak-floor: not in the slice.
- Whether claiming feels like a small surprise: the playtest's job.

## Run log

| Date | Build | Who | Cases run | Pass | Fail | Blocked | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-21 | build 0.1.7 | QA Lead | 5 | 4 | 0 | 1 | TC-F001.server-time-01 blocked: endpoint stubbed |
