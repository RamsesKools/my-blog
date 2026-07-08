---
date: 2026-07-08
slug: agent-config
---

# How to configure your local coding AI agents once

I use three AI coding agents: [Claude Code](https://code.claude.com/docs/en/overview), [Codex](https://developers.openai.com/codex/cli/), and [GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli).
Each one wants its own global config in its own location, in its own format.
Configuring my preferences multiple times, and keeping them in-sync between machines and agents was starting to become a problem for me.
So all of it now lives in one `~/.agents` folder and repo, and every agent reads from there.

<!-- more -->

## What is a coding agent anyway?

New to this? Here is a quick explanation.
A coding agent is an LLM-powered tool that runs on your machine, in your terminal or IDE.
Instead of copy-pasting snippets into a chat window, the agent reads your files, runs commands, writes code, and debugs its own work.
The catch: an agent is only as good as the context and instructions you give it.
Tell it once how you like to work and it stops asking, which is exactly what all this configuration is about.

## Two layers of agent config

The first thing to get right is what belongs where.
Agent configuration comes in two layers:

1. **Project config** lives in each repo: an `AGENTS.md` or `CLAUDE.md` describing that project's architecture, commands, and conventions.
It belongs to the project and travels with it.
2. **Global config** is about me, not any project: my writing style, my preferred tone, my markdown conventions, my personal skills.
It should follow me across machines and apply in every repo.

The global layer is the one that gets messy.
Without a system it ends up scattered over `~/.claude/`, `~/.codex/`, and whatever Copilot reads, drifting apart per tool and per machine.
That is exactly the same problem classic dotfiles solve for shell config, which is why this repo is a natural sibling of [my computer-setup repo](computer-setup.md).

## More than a context file

Agent config is also more than just an `AGENTS.md`.
Each tool has a whole surface of things to configure:

- **Context**: the `AGENTS.md` / `CLAUDE.md` instructions themselves, loaded at the start of every session.
- **Settings and permissions**: which commands the agent may run without asking, which files and directories it may read, environment variables.
- **Skills**: reusable task instructions the agent loads on demand, following the [Agent Skills standard](https://agentskills.io/).
- **MCP servers**: connections to external systems like GitHub, Jira, or your calendar.
- **And more**: hooks that run shell commands at key moments, custom subagents with their own model and tool access, slash commands, model preferences.

Skills deserve a special mention, because they get really powerful when you pair them with a CLI tool.
A small skill that teaches the agent the [`gh` CLI](https://cli.github.com/) suddenly lets it work with pull requests, issues, and workflow runs, no MCP server needed.

My repo currently covers the first three: the shared context file, a `skills/` folder all agents read, and a sanitized settings template for the permission rules.
The rest still lives per tool, which says something about how young this space is (more on that below).

## One repo, three agents

The `~/.agents` repo is the single source of truth:

```text
~/.agents/
├── AGENTS.md          the actual global agent context
├── CLAUDE.md          one-liner: @AGENTS.md (compat for Claude Code)
├── skills/            personal skills, shared by all three agents
├── settings/          sanitized Claude settings template
└── scripts/
    ├── setup-symlinks.sh          wires everything up
    └── strip-claude-settings.sh   regenerates the settings template
```

Each tool reads from it in its own way:

| Tool | What it reads | How |
| --- | --- | --- |
| Claude Code | `~/.claude/CLAUDE.md`, `~/.claude/skills/` | symlinks |
| Codex | `~/.codex/AGENTS.md`, `~/.codex/skills/` | symlinks |
| Copilot CLI | `~/.agents/skills/` | native, no symlink needed |

`setup-symlinks.sh` creates the symlinks and is idempotent.
Any pre-existing real file is backed up before being replaced, so running it never loses data.
On a fresh machine I don't even run it myself: the `fresh.sh` bootstrap from [my computer-setup post](computer-setup.md) clones this repo and runs it as one of its steps.

The result: edit `AGENTS.md` once, commit, and all three agents pick it up on their next session, on every machine.

## AGENTS.md standardization

The file format at the center of this is [AGENTS.md](https://agents.md/), an open standard for agent instructions.
It has genuinely become the standard: over 60,000 open-source projects have adopted it, and in December 2025 OpenAI contributed it to the newly formed [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-agentic-ai-foundation) under the Linux Foundation, alongside Anthropic's [MCP](https://modelcontextprotocol.io/).
Codex, Copilot, Cursor, and most other coding agents read it natively.

Claude Code is the notable holdout: it still wants a `CLAUDE.md` (tracked in [anthropics/claude-code#6235](https://github.com/anthropics/claude-code/issues/6235)).
The documented workaround is a `CLAUDE.md` containing exactly one line:

```markdown
@AGENTS.md
```

The `@` import makes Claude Code read the shared file, and the standard keeps everything else vendor-neutral.

## What deliberately stays out

Just as important as what is in the repo is what is not:

- **Machine-specific settings.**
My live `~/.claude/settings.json` accumulates absolute paths and per-machine permissions.
A small `strip-claude-settings.sh` script regenerates a sanitized template from it, stripping anything that references my home directory.
The template is committed, the live file is not.
- **MCP server configs.**
The format differs per tool (JSON for Claude, TOML for Codex, another JSON layout for Copilot), so they cannot be shared through symlinks yet.
- **Runtime state.**
Sessions, logs, caches, and auth tokens are never portable and never belong in git.

## A young, messy space

Managing this local layer across multiple agent frameworks gets messy fast, and I am clearly not the only one who noticed.
There is a small ecosystem forming around the same idea:

- [dot-agents](https://www.dot-agents.com/) turns the `~/.agents/` directory into a full config layer for Cursor, Claude Code, Codex, and more.
- [mfmezger/ai_agent_dotfiles](https://github.com/mfmezger/ai_agent_dotfiles) is a dotfiles repo for agent configs covering Claude Code, Codex, OpenCode, and Gemini CLI.
- [yzhao062/agent-config](https://github.com/yzhao062/agent-config) takes a generation approach: one `AGENTS.md` as source, per-agent files generated from it.
- [AgentsMesh](https://samplexbro.github.io/agentsmesh/) goes furthest: write rules, skills, MCP servers, and permissions once, then generate native config for 15+ tools.
- [agentsync](https://github.com/dallay/agentsync) is a CLI that symlinks configs, skills, and MCP definitions from a central `.agents/` directory into each tool's location.
- [ruler](https://github.com/intellectronica/ruler) merges rule files from a `.ruler/` directory and distributes them to 30+ agents with one `ruler apply`.
- [Kaushik Gopal's aikado setup](https://kau.sh/blog/agents-md/) is another take on the symlink approach: one personal repo that every tool's config path points back to.
- [This dev.to post](https://dev.to/opensite/how-to-sync-ai-coding-agent-skills-across-every-platform-one-repo-zero-copy-paste-ba0) even syncs skills to cloud agents via browser automation, because there is no API for it.

That list also shows how immature this space still is.
Everyone is inventing their own bridge between the same handful of tools.
I hope the AI providers will eventually agree on shared standards for settings and permissions, like they did for context ([AGENTS.md](https://agents.md/)) and skills ([Agent Skills](https://agentskills.io/)).
Until then, custom tools that sync configs, context, and settings across agent frameworks are going to be brittle, with things changing rapidly on all ends.

That is why I kept my own approach as simple as possible.
Plain symlinks are the easiest and most straightforward way to do this, and I don't think my approach is necessarily the best: it still lacks proper syncing of settings between frameworks.
But at least all my changes are visible in a single repo, and I can track them.

## An example to look at

Fair warning: my `~/.agents` repo is quite new and not very fleshed out yet.
This is iteration one, built for exactly the three agents I use today.
The repo itself is private, but I published a depersonalized snapshot at [github.com/RamsesKools/agent-config-example](https://github.com/RamsesKools/agent-config-example).
I don't intend to keep that example very up to date, but it shows what my current setup looks like.

And in the meantime the loop keeps running: every time I catch myself explaining a preference to an agent twice, that preference moves into `AGENTS.md`.
