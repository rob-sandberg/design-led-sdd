# 01. The loop

How a game team works with AI agents in the prototype tier. The designer directs and decides; agents do most of the hands-on work.

## Three rules

1. **Give the agent hands on the real project.** Editor, builds, logs, data. An agent that can only edit files is guessing.
2. **Prove it on the real target.** A device, an emulator, a playable build. "It compiled" is not proof, and neither is "the tests pass" when nobody has played it.
3. **Write down what you learn the same day, with the reason.** Every session starts from facts, not from zero. Every mistake becomes a rule.

## The loop

1. **Spec first.** Search the specs. Settle small gaps yourself; raise real design decisions as open questions.
2. **Choose the path.** Short path for a small change (a brief). Full path for a new feature or system (a feature spec).
3. **Clarify.** No feature leaves Draft while it has an Open question that blocks it.
4. **Analyse.** Check the spec against the constitution, the glossary and the other specs before anything is built.
5. **Break it down** into job stories with acceptance criteria.
6. **Build** on a branch, in small slices that can be played.
7. **Prove it** on the target, then **review**. Never ship what you cannot explain.
8. **Playtest and revise.** What the build teaches you goes back into the spec, not into a chat.
9. **Write it down**: state file, decisions, new rules.

The loop goes round, not down. Steps 6 to 8 repeat until the feature is fun, then the spec is the record of why it is the way it is.

## Two paths

| | Short path | Full path |
| --- | --- | --- |
| Use for | A fix, a tweak, a tuning pass, one slice of a feature | A new feature, a new system, anything another discipline builds on |
| Artefact | One brief (`specs/briefs/`) | Feature folder: `spec.md`, `tasks.md`, `playtest-log.md` |
| Gates | Read the constitution; prove it on the target | Clarify, analyse, ready check, prove, playtest |
| Skill | `brief` | `spec`, `clarify`, `analyze`, `tasks`, `playtest` |

If a brief grows past one page, it is a feature. Promote it.

## Roles

| Role | Does |
| --- | --- |
| Designer or producer (the human) | Priorities, design calls, approves anything irreversible or public, reviews what ships |
| Lead agent | One long session: plans, writes briefs, reviews, keeps the specs and state file current |
| Helper agents | One briefed task each, then stopped. At most two at once, never on the same files |
| Scheduled agent | Runs on a timer for checks and summaries |

Larger teams can add named specialist agents. The rules in `02-who-decides.md` still hold.
