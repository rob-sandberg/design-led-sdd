# 06. Two starts: a new game or an existing one

The method has two entry points, because the truth lives in different places.

| | New game | Existing game |
| --- | --- | --- |
| Where the truth is | In people's heads and a pitch | Spread across code, design docs, tickets, wikis and the build |
| First job | Write down intent | Take stock of what exists, and what is actually true |
| Skill | `constitution` | `adopt` |
| Constitution | Built from questions | Drafted from existing docs and code, then confirmed |
| Glossary | Invented as you go | Pulled from code and UI; mismatches become open questions |
| Open questions | Start empty | Imported from existing registers, plus contradictions between docs |
| Feature specs | Written before building | Written when a feature is next touched |
| A spec's "Today" section | Usually "Nothing" | The most important section: what the build does now |
| Biggest risk | Specs that never meet a build | Specs that describe the game as documented, not as built |

## Spec the change, not the game

On an existing game, never backfill specs for the whole game. It takes weeks, it is out of date before it is finished, and nobody reads it.

Instead, a feature gets a spec the first time it is changed. The spec is written from the current build plus the change. Everything untouched stays in its old documents, which `specs/sources.md` maps to features so agents know where to look. Coverage grows where the work is.

## The build beats the document

When an old document and the build disagree, the build is what players have. Record what the build does in "Today", raise the disagreement as an open question, and let the designer decide which one was right. Never quietly "fix" either side.

## Live games

A game that is already live, with real players and real money, should consider the production tier for its economy, rewards and purchases from the start. See `05-two-tiers.md`.
