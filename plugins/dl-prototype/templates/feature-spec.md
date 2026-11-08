# F[NNN]: [Feature name]

- Status: Draft | Ready | In build | In playtest | Settled | Graduated
- Owner: [role title]
- Last updated: YYYY-MM-DD
- Links: [design file] · [prototype] · [tickets]

## Intent

[Why this feature exists, in two or three sentences. Which design pillar it serves.]

## Player experience

[What the player feels and does, in plain words. The moment that should land. What failure feels like for the player, and what it must not feel like.]

## Today

[What happens now, before this feature. "Nothing" is a valid answer for a new game.]

## Scope

- In: [...]
- Out, for now: [deliberately left for later; will come back]
- Out, for good: [the game will never do this; also add to the constitution if it is game-wide]

## Job stories

1. When [situation], I want to [goal], so I can [outcome].
2. [...]

## Rules

### F[NNN].[short-id]: [Rule in one sentence]

```gherkin
When      [event]
Provided  [condition]
Then      [what happens when it holds]
Otherwise [what happens when it does not]
```

| situation | provided | outcome | why |
| --- | --- | --- | --- |
| [concrete case] | yes | [result] | |
| [concrete case] | no | [result] | |

[Repeat per rule. Use `?` for anything undecided.]

## States

| State | What the player sees | How they get here | How they leave |
| --- | --- | --- | --- |
| Default | | | |
| Empty | | | |
| Loading | | | |
| Error | | | |

## Parameters

Tuning values live here, not inside rules, so playtests can change them without rewriting rules.

| Name | Value | Unit | Notes |
| --- | --- | --- | --- |
| [daily_gift_reset] | [00:00] | [local time] | |

## Terms

New or special words this feature uses. Add them to `specs/glossary.md` too.

| Term | Means |
| --- | --- |

## Playtest hypotheses

What we expect to learn by playing it. Each one is checked in `playtest-log.md`.

1. If [we build X], then [players will Y], measured by [observation or metric].

## Dependencies

| Needs | From | Status |
| --- | --- | --- |
| [asset, API, other feature] | [discipline or feature ID] | [Done / In progress / Risk accepted] |

## Risks

- If [condition], then [consequence].

## Open questions

See `specs/open-questions.md`, rows `OQ-F[NNN]-*`. Blocking questions keep this spec in Draft.

## Changelog

| Date | Change | By |
| --- | --- | --- |
| YYYY-MM-DD | First draft | [role] |
