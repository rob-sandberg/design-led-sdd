# F[NNN]: [Feature name], tasks

- Built from: `spec.md` as of YYYY-MM-DD
- Ticket system: [Jira key / GitHub Issues / none]

Each story is ready to paste into a ticket. Tasks sit under their story.

## Story S1: [short title]

**Job story:** When [situation], I want to [goal], so I can [outcome].

**Spec rules:** F[NNN].[id], F[NNN].[id]

**Acceptance criteria**

```gherkin
Scenario: [Happy path]
  Given [starting state]
  When  [action]
  Then  [observable result]

Scenario: [Guard: the condition does not hold]
  Given [...]
  When  [...]
  Then  [...]

Scenario: [Error]
  Given [...]
  When  [...]
  Then  [...]
```

**Tasks**

| ID | Discipline | Task | Depends on |
| --- | --- | --- | --- |
| S1.T1 | Design | [...] | |
| S1.T2 | Art | [...] | S1.T1 |
| S1.T3 | Engineering | [...] | S1.T2 |
| S1.T4 | QA | [...] | S1.T3 |

**Proved by:** [how a designer or producer will play it to call it done]

---

[Repeat per story.]

## Not ticketed

- [Parts of the spec deliberately left for a later round, with the reason.]
