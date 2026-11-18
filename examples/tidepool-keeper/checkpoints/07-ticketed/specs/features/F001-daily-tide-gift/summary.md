# Daily tide gift, in plain words

- Feature: F001 ([spec](spec.md))
- Status: Ready
- Written: 2026-11-19, against spec revision rev-d2ee83c64152, for readers outside the team. The spec is the source of truth.

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
