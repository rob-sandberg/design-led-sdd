---
name: playtest
description: Record a playtest session for a game feature, tie observations to hypotheses and decisions, and turn accepted changes into spec revisions, handling what that does to the feature's Ready approval and its tickets. Use after anyone plays a build, when someone shares playtest notes, feedback, recordings or metrics, or asks how a playtest should change the design.
---

# Playtest

Closes the loop. What the build teaches goes back into the spec, so the spec stays the record of why the feature is the way it is. A change after approval follows `principles/03-ready-and-done.md`, "When the spec changes after approval".

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/`, `templates/` and `scripts/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

## Steps

1. Read the spec (its Playtest hypotheses, Parameters and Approval), `tasks.md` (which slice was built and ticketed) and `playtest-log.md` if it exists.
2. Check the hypotheses match what was built. A hypothesis about something outside the ticketed slice cannot be tested in this session: mark it Not tested and say why.
3. Before looking at the results, write for each hypothesis what observation would count as Held and what as Failed.
4. Take the notes in whatever form they come. Separate what players did (observation) from what people said (opinion). Ask about anything unclear, one question at a time.
5. Mark each hypothesis Held, Failed or Unclear, with the evidence. Use Unclear when the evidence cannot settle it.
6. Propose spec changes, sorted by kind, each citing the observation it comes from:
   - **Tuning:** a parameter value changes.
   - **Rule:** a rule's condition, outcome or examples change, or a rule is added or removed.
   - **Scope:** something moves in or out.
   - **Pillar:** the playtest challenges a design pillar. Flag it to the designer; do not change the constitution from here.
7. Ask the designer to accept, change or reject each proposal, one at a time, as multiple choice with the recommended option first.
8. Write the session at the top of `playtest-log.md`, then apply the accepted changes to the spec, each with a changelog row naming the session.
9. Run `spec_diff.py <spec> --since <the approval's commit> --tasks <tasks.md> --test-plan <test-plan.md>`, and record in the session which revision it produced and which stories it touches.
   - **Rule or scope change:** approval has lapsed. Set the spec's Status to Draft, each touched story's Status to `Recheck: <rule IDs>`, and each listed test case's Status to Stale. Work already in progress keeps its record. List the tickets to update. The spec goes back through `analyze` and the designer's approval before new or revised work is handed off.
   - **Tuning only:** if the stories that name the parameter still pass their acceptance criteria as written and no other feature relies on the old value, ask the designer whether to carry the approval over; on a yes, record it as principle 03 describes. If a criterion or another feature depends on the value, say so and treat it as a rule change.
10. Write the hypotheses for the next session.

## Graduation check

After writing the session, check `principles/05-two-tiers.md`. If the feature now meets a graduation condition (for example, the last two sessions changed only tuning values, and it handles currency, rewards or purchases), say so and suggest moving it to the production tier.

## Do not

- Change rules on the strength of one player's opinion. Record it; change on evidence.
- Lose the reason. Every spec change from a playtest names its session and observation.
- Carry an approval over without the designer's yes.
