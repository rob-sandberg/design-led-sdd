# Tidepool Keeper: the worked example as files

Tidepool Keeper is a fictional cosy mobile game. Feature F001, the daily tide gift, goes once round the prototype loop. Each folder in `checkpoints/` is the project's complete `specs/` folder at one moment, so you can open any step, run the scripts on it and see what the method expects.

The story is told in [`docs/worked-example.md`](../../docs/worked-example.md). These files are what it describes.

## Checkpoints

| Folder | Moment | Ready check: approve / ticket / story S1 |
| --- | --- | --- |
| `01-start` | Constitution, glossary, empty register | (no spec yet) |
| `02-draft` | First draft; two blocking `?` places | Fail / Fail / - |
| `03-clarified` | Questions answered; Clarify found the offline gap and added a rule | Fail (no analysis) / Fail / - |
| `04-analysed` | First analysis: one blocking finding | Fail / Fail / - |
| `05-reviewed` | Finding fixed; focused rerun on the new revision | Pass / Fail (not approved) / - |
| `06-approved` | The Lead Designer approves the spec | Pass / Pass / - |
| `07-ticketed` | Story S1 (claiming only), test plan, test room, summary | Pass / Pass / Pass |
| `08-proved` | Built and hand-tested on the emulator | Pass / Pass / Pass |
| `09-tuned` | Playtest; `reset_time` 05:00 to 04:00; approval carried over | Pass / Pass / Pass |
| `10-revised` | Countdown dropped: a rule change, so approval lapses | Fail / Fail / Fail |

## Try it

From the repo root, step into a checkpoint and run the check. Every command names the feature folder relative to that checkpoint.

```
cd examples/tidepool-keeper/checkpoints/04-analysed
python3 ../../../../plugins/dl-prototype/scripts/ready_check.py specs/features/F001-daily-tide-gift --stage approve --root .
```

To compare two moments:

```
cd examples/tidepool-keeper/checkpoints
python3 ../../../plugins/dl-prototype/scripts/spec_diff.py 10-revised/specs/features/F001-daily-tide-gift/spec.md --old 09-tuned/specs/features/F001-daily-tide-gift/spec.md --tasks 09-tuned/specs/features/F001-daily-tide-gift/tasks.md --test-plan 09-tuned/specs/features/F001-daily-tide-gift/test-plan.md
```

`tests/test_fixture.py` checks every result in the table above. The files are built by `tools/make_fixture.py`, which computes the revisions rather than typing them, so they always agree with the spec text.

## What the example does not show

- A real ticket system. Tickets stay in `tasks.md`.
- Commits. Approvals record `Commit: working copy`, so a carried-over approval is not verified against git here; the Ready check warns about that. In a real repo, record the commit.
- Code. The build is described in brief B001's report, not included.
