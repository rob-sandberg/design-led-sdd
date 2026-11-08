# 02. Who decides

Agents write faster than anyone can review. The method stays sane only if it is always clear who makes which call, and every call lands in a spec.

| Who | Decides | Never |
| --- | --- | --- |
| Client or product owner | What the game should do, what a word means, what is in or out of scope | Has to read the specs to approve something; gets a plain summary instead |
| Designer | How a request becomes a spec, every design gap the agents find, playtest conclusions | Leaves a decision in a chat or a head instead of the spec |
| Producer | Priority, scope per milestone, what is ready, what is done | Overrides a spec silently; raises an open question instead |
| Agents | Nothing about the game. They report what the spec did not decide | Fill a design gap with a guess and carry on |

## Rules that follow

- **An agent that meets a gap stops and reports it**, with a recommendation. It may take a harmless default only for things the constitution says are agent calls (naming, file layout, code style).
- **Business questions go to the owner, not to the agent or the designer.** The place stays open (`?`) until the owner answers.
- **Nothing found is mentioned once and dropped.** Every hole ends either decided in the spec, or open in `specs/open-questions.md` with an owner.
- **Spec conflicts are raised, not resolved quietly.** If work conflicts with a spec, raise an open question and flag it to the producer.
- **Ask one question at a time**, as multiple choice with the recommended option first.
