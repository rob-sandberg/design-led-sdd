# 03. Ready and done

The minimum bar. If a piece of work does not meet Ready, it stays in the queue. If it does not meet Done, it does not move to Done. Work that fails review does not move backwards: raise a new item for the rework.

## Feature spec: Ready

A feature spec is Ready to break into tasks when:

1. Intent, player experience and scope (in and out) are written
2. Every rule has at least one example
3. No open question marked **Blocking** is still Open
4. Every term the spec uses with a special meaning is in the glossary
5. `analyze` has run on its final state with no unresolved finding
6. The designer has marked it Ready in its status line

## Universal Ready (any task or ticket)

1. Title follows the project's naming convention
2. It links to its spec or brief
3. Acceptance criteria are written: at least three points, describing what, not how
4. Its parent story is linked (tasks only)
5. Dependencies on other disciplines are named and either done or explicitly accepted as a risk

## Universal Done

1. All acceptance criteria are met and verified on the target
2. Reviewed by at least one other person (or a separate checking agent, for agent work)
3. No known defect blocks the next discipline in the chain
4. A one-sentence completion note says what was delivered
5. Any decision or deviation from the spec is written into the spec or raised as an open question

## Story Done

1. All its tasks are Done
2. The player can do what the job story says, in a playable build
3. A designer or producer has played it, not just ticked the tasks
4. Its happy path, guard and error scenarios all pass

## Discipline additions

Add discipline-specific Ready and Done lines in the project constitution (section "Ready and done additions"). Typical ones:

- **UI design:** all screen states documented (default, empty, loading, error, edge cases)
- **Art:** assets exported to the agreed format and committed to the agreed place
- **Engineering:** no regressions; reviewed by a second engineer or checking agent
- **QA:** pass or fail per acceptance criterion, with the build version tested
