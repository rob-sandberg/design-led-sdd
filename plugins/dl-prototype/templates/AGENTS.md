# AGENTS.md: [GAME NAME]

Rules for any AI agent working in this repository. Claude Code reads this through `CLAUDE.md`; other agents read it directly.

## Before anything

1. Read `specs/constitution.md`.
2. Read `specs/STATE.md` if it exists. It says where the work is.
3. For any change, find its spec or brief in `specs/`. If none exists, ask whether this is a brief (small) or a feature (large) before writing code.

## While working

- Build from the spec. Where the spec does not decide something, stop and report the gap with a recommendation, unless the constitution lists it as an agent call.
- Never change a spec's meaning silently. Raise an open question in `specs/open-questions.md`.
- Mark undecided places with `?`. Nothing with a blocking `?` is built.
- Prove work on the target named in the constitution. Say how you proved it.
- Ask one question at a time, as multiple choice with the recommended option first.

## After working

- Update the spec's changelog (newest row at the top) and `specs/STATE.md`.
- Write down anything learned that the next session needs, with the reason.
- Turn a mistake into a rule here or in the constitution.

## Never

- Anything listed under "Ask first" or "Never" in the constitution, without a yes.
- Agent names in documents outside readers will see. Use role titles.
