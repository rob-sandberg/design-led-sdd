# Analysis: F[NNN] [Feature name] (YYYY-MM-DD, run NN)

- Spec revision: rev-xxxxxxxxxxxx
- Spec commit: [short hash, or "working copy"]
- Context: constitution rev-xxxxxxxxxxxx, glossary rev-xxxxxxxxxxxx
- Inputs: [every file the reviewer was given]
- Access: [what the reviewer could use, e.g. "Read only; inputs passed by the lead; no shell, network or connectors"]
- Run by a separate reviewer that saw only the inputs above, not code, tests, tickets, chats or earlier reports.

File name: `analysis-YYYY-MM-DD-NN.md`, NN counting runs on the same day from 01. Never overwrite an earlier report.

## Verdict

[Clean | Findings to resolve: N blocking, N advisory]

## Findings

| # | Kind | Where | Finding | Evidence | Suggested fix | Severity |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Contradiction / Gap / Untestable / Unmarked term / Pillar or scope conflict / Missing Otherwise / One-sided examples / Value inside rule / Dependency | [rule ID or section] | [...] | [quoted text or line] | [...] | Blocking / Advisory |

Blocking: a builder or tester would build or test the wrong thing, or stall. Everything else is Advisory. Wording notes that change no meaning go in the list below, not the table.

Wording notes:

- [...]

## Checked and found consistent

[One paragraph.]

## Other features this may affect

| Feature | Why it may be affected | Checked |
| --- | --- | --- |

## Not checked

- Feel, pacing, visual quality and fun, which are judged by playing.
- Whether the build matches the spec (the build-checker's job).

## Resolutions

Filled in by the lead with the designer's decisions. A blocking finding is resolved by an edit (which makes a new revision, checked again) or dismissed with a reason and a named decision-maker. Advisory findings may stay Open.

| # | Disposition | Reason | Decided by | Date |
| --- | --- | --- | --- | --- |
