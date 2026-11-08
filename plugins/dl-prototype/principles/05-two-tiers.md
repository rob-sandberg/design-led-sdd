# 05. Two tiers

The method has two tiers, because a game changes character as it moves from finding the fun to shipping and running live.

| | Prototype tier (this plugin) | Production tier (planned) |
| --- | --- | --- |
| Purpose | Find the fun fast, keep decisions visible | Keep rules true across many changes |
| Spec shape | Feature folders, guarded rules where they matter | Spec tree of capabilities, features and rules with stable IDs |
| Change control | Specs revised after each playtest | Every change is an amendment on a branch, diffed against a baseline |
| Checking | `analyze` reads specs for consistency | Mechanical impact analysis plus an independent checking agent |
| Testing | Played on the target; acceptance criteria | Independent testing and coding agents; tests checked with mutants |
| Overhead | Low | High, on purpose |

The production tier is modelled on Bruno Baketarić's Proviso. It will ship as a second plugin in this marketplace.

## When a feature graduates

Move a feature to the production tier when any of these is true:

- Getting a rule wrong costs real money or trust: economy, rewards, purchases, ads, progression, resolution of outcomes, age gates, legal and consent
- Other features keep breaking when this one changes
- The feature is live and will be changed by people who did not design it
- Playtests have stopped changing its rules and only change its tuning values

Visual and feel work (layout, juice, animation, art direction) stays in the prototype tier for the life of the game. It is judged by playing it, not by rules.

## Writing for graduation now

Three habits in the prototype tier make graduation cheap:

1. Write rules in the guarded form with an `Otherwise`.
2. Give every rule a short, stable ID in its heading (`F003.claim-once`).
3. Keep tuning values (timers, rewards, prices) in the spec's Parameters table, not inside rule text.
