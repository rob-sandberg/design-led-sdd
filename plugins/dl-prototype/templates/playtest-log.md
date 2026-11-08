# F[NNN]: [Feature name], playtest log

Newest session at the top. Each session ends with what changed in the spec, so the spec stays the record of why the feature is the way it is.

## Session N: YYYY-MM-DD

- Build: [version or commit]
- Who played: [roles or player profile, number of players]
- What we tested: [hypotheses from the spec, by number]

### What we saw

- [Observation, as fact, not opinion.]

### Hypotheses

| # | Hypothesis | Result | Evidence |
| --- | --- | --- | --- |
| 1 | | Held / Failed / Unclear | |

### Spec changes

| Spec part | Change | Kind |
| --- | --- | --- |
| Parameters: [name] | [old] to [new] | Tuning |
| Rule F[NNN].[id] | [what changed] | Rule |
| Scope | [moved X to Out, for now] | Scope |

- Tuning changes: apply directly, note them here.
- Rule or scope changes: apply to the spec, rerun `analyze`, and check which tasks and tickets they affect.

### Next session tests

1. [...]
