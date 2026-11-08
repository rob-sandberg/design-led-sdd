---
name: playtest
description: Record a playtest session for a game feature and turn what was learned into spec changes. Use after anyone plays a build, when someone shares playtest notes, feedback, recordings or metrics, or asks how a playtest should change the design.
---

# Playtest

Closes the loop. What the build teaches goes back into the spec, so the spec stays the record of why the feature is the way it is, and the next build starts from it.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

## Steps

1. Read the spec (especially Playtest hypotheses and Parameters) and the feature's `playtest-log.md` if it exists.
2. Take the notes in whatever form they come. Separate what players did (observation) from what people thought (opinion). Ask about anything that is unclear, one question at a time.
3. Mark each hypothesis Held, Failed or Unclear, with the evidence.
4. Propose spec changes, sorted by kind:
   - **Tuning:** a parameter value changes. Low risk.
   - **Rule:** a rule's condition or outcome changes, or a rule is added or removed.
   - **Scope:** something moves in or out.
   - **Pillar:** the playtest challenges a design pillar. Flag it to the designer; do not change the constitution from here.
5. Ask the designer to accept, change or reject each proposal, one at a time, as multiple choice with the recommended option first.
6. Write the session at the top of `playtest-log.md` (from `playtest-log.md` if new), then apply the accepted changes to the spec with a changelog row each.
7. For rule or scope changes: list the tasks and tickets affected and offer to run `analyze`.
8. Write the hypotheses for the next session.

## Graduation check

After writing the session, check `principles/05-two-tiers.md`. If the feature now meets a graduation condition (for example, the last two sessions changed only tuning values, and it handles currency, rewards or purchases), say so and suggest moving it to the production tier.

## Do not

- Change rules on the strength of one player's opinion. Record it; change on evidence.
- Lose the reason. Every spec change from a playtest says which session and observation it came from.
