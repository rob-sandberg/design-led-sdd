# dl-prototype 0.3 smoke test

The scripts in 0.3 are covered by automated tests. The skills and agents need a live Claude Code session, which the build environment did not have. Run these checks once in Claude Code before relying on 0.3. Each takes a few minutes. Use a throwaway copy of a checkpoint, never a real project.

## Set-up

1. Copy `examples/tidepool-keeper/checkpoints/04-analysed` to a new folder outside the repo and open Claude Code there.
2. Start Claude Code with the plugin: `claude --plugin-dir <repo>/plugins/dl-prototype`.

## Checks

| # | Do | Expect | Result |
| --- | --- | --- | --- |
| 1 | Type `/` and look for the dl-prototype skills | All eight skills listed | |
| 2 | Type `/agents` | `spec-analyst` and `build-checker` listed | |
| 3 | Ask: "is F001 ready?" | Claude runs `ready_check.py` and reports one blocking finding | |
| 4 | Run `/dl-prototype:analyze` on F001 | A new `analysis-2026-…-NN.md` naming the current revision; the Access line says the reviewer was Read only | |
| 5 | Add a contradicting line to the glossary first, then repeat 4 | The report finds the contradiction | |
| 6 | Ask the spec-analyst to open a file it was not given | It declines or says it works only from pasted inputs | |
| 7 | Run `/dl-prototype:clarify` | It asks for approval before writing the Approval section; say no, and nothing is written | |
| 8 | Put your own `tasks.md` in `specs/overrides/templates/`, then run `/dl-prototype:tasks` | Your template is used | |
| 9 | In `06-approved`, run `/dl-prototype:tasks` | Story S1 written as Draft, a test plan with one case per example row, and a request to approve the story | |
| 10 | Install from the marketplace: `/plugin marketplace add <repo path>`, then `/plugin install dl-prototype@design-led-sdd` | Installs as version 0.3.0 | |

Record anything unexpected as an issue, with the checkpoint and the step.
