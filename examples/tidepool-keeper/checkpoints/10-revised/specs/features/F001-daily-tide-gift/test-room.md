# F001 test room

- Status: Approved by Lead Designer 2026-11-19
- For: `tasks.md` story S1; every case in `test-plan.md`
- Spec: revision rev-d2ee83c64152
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
