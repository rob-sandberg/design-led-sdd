# Design-led SDD

Spec-driven development for game teams working with AI agents, led by design rather than by code.

Most spec-driven tools assume software features: write a spec, plan, break into tasks, build, done. Games do not work that way. They find their design by being played, so the spec has to change after every playtest without losing the reasons behind it. This method keeps the discipline of a spec (agents build from it, gaps are visible, decisions are written down) and adds the loop games need.

It ships as a Claude Code plugin marketplace with two tiers:

| Plugin | Tier | Status |
| --- | --- | --- |
| `dl-prototype` | Prototype: light specs for finding the fun | 0.1.0, first version |
| `dl-production` | Production: rules kept true across many changes | Planned |

See `plugins/dl-prototype/principles/05-two-tiers.md` for when a feature moves from one to the other.

## Install

In Claude Code:

```
/plugin marketplace add <path or git URL of this repo>
/plugin install dl-prototype@design-led-sdd
```

To try it locally without installing: `claude --plugin-dir ./plugins/dl-prototype`

## Use it

Start in a game project and run the skills in Claude Code. Each one asks one question at a time, as multiple choice.

| Skill | What it does |
| --- | --- |
| `/dl-prototype:constitution` | Sets up the project: constitution, AGENTS.md, open questions, glossary, state file |
| `/dl-prototype:spec` | Full path: writes or revises a feature spec |
| `/dl-prototype:brief` | Short path: one-page brief for a small change, optionally handed to a helper agent |
| `/dl-prototype:clarify` | Works through open questions until a spec can be marked Ready |
| `/dl-prototype:analyze` | Independent consistency check across specs; read-only |
| `/dl-prototype:tasks` | Job stories, Gherkin acceptance criteria and per-discipline tasks, ready for tickets |
| `/dl-prototype:playtest` | Records a playtest and turns it into spec changes |

You can also just describe what you want ("spec out a daily gift feature", "we playtested the shop, here are the notes"); the skills load from their descriptions.

## What it puts in your project

```
AGENTS.md                     rules for any agent, read first
CLAUDE.md                     @AGENTS.md
specs/
  constitution.md             the game in one screen: pillars, platforms, boundaries, agent rules
  STATE.md                    where the work is; read first every session
  glossary.md                 words with a special meaning
  open-questions.md           every undecided place, with an owner
  features/F001-name/
    spec.md                   intent, experience, scope, rules, states, parameters
    tasks.md                  stories and tasks for tickets
    playtest-log.md           what each playtest changed, and why
    analysis-YYYY-MM-DD.md    consistency check reports
  briefs/B001-name.md         short-path changes
  overrides/templates/        your versions of any template; these win
```

## Customising

The method is shared; your project's choices are not. Three layers, highest first:

1. **Project overrides:** a file in `specs/overrides/templates/` with the same name as a plugin template replaces it for that project.
2. **Project layer:** your constitution, glossary and specs.
3. **Method:** this plugin's principles and templates. Update the plugin to get improvements; you never edit it inside a project.

## Where it comes from

- The working method behind a mobile game at Gamefuel Studio: the AI-first development loop, job stories with Gherkin acceptance criteria, Definitions of Ready and Done, the open questions register and spec conventions.
- [GitHub Spec Kit](https://github.com/github/spec-kit): the constitution, the clarify and analyse gates, a short and a full path, tasks handed to tickets, and layered overrides.
- [Proviso](https://github.com/bbak/proviso) by Bruno Baketarić: guarded rules with `Otherwise`, undecided places that block building, who decides what, and checking agents kept apart from the work. The production tier will draw on it much further.

## Repository layout

```
.claude-plugin/marketplace.json
plugins/dl-prototype/
  .claude-plugin/plugin.json
  principles/       the method, for people
  templates/        the shapes the skills fill in
  skills/           the procedures, for agents
examples/           a small fictional game, to show the format
CHANGELOG.md
```

## Licence

Not yet decided. All rights reserved until a licence is added.
