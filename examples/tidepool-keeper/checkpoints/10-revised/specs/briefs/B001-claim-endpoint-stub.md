# B001: Stub the claim endpoint (2026-11-20)

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
