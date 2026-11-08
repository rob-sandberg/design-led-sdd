---
name: brief
description: Write a one-page task brief for a small change to a game (the short path of the design-led prototype method), and optionally hand it to a helper agent. Use for fixes, tweaks, tuning passes, a single slice of an existing feature, or any change that fits on one page. For a new feature or system, use the spec skill.
---

# Brief

The short path. One page, one helper, one change, proved on the target.

## Where things come from

This plugin's folders sit two levels up from this skill's folder: `principles/` and `templates/`. For any template, use `specs/overrides/templates/<file>` in the project if it exists, otherwise the plugin's `templates/<file>`.

## Steps

1. Read `specs/constitution.md` and `specs/STATE.md`.
2. Find the feature spec this change touches, if any, and read the rules it affects.
3. Check the size. If the change needs new rules, touches more than one feature, or another discipline builds on it, suggest the `spec` skill instead.
4. If the change contradicts a spec rule, stop: either the spec changes first (offer to revise it) or the brief changes.
5. Write `specs/briefs/B<NNN>-<short-name>.md` from `brief.md`. Context must be complete: a fresh helper reads only this file and the files it names.
6. Make the last step "Prove it", naming the target from the constitution.
7. Fill "Not in this brief" with anything adjacent the helper might be tempted to do.
8. Ask whether to start a helper agent on it now. If yes, start one helper with the brief as its whole instruction, and stop it when it reports.
9. When the helper reports, check its proof, update `specs/STATE.md`, and if it found a gap in a spec, raise an open question.

## Keep it to a page

If the brief will not fit on one page, it is a feature. Say so and offer to promote it.
