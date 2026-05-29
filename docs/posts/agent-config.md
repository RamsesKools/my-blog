---
date: 2026-05-29
draft: true
---

# How to configure all your AI-Agents once

*Dealing with different agent frameworks and staying coding agent framework agnostic.*

I switch between [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://github.com/openai/codex), and [GitHub Copilot](https://github.com/features/copilot) depending on the project.
Each one wants its own config files in its own place, in its own format.
This post is about how to personalize all your AI-Agents in one place.

<!-- more -->

## Two types of AI-Agent personalization

There are really two configuration problems to solve:

1. **System-wide setup**: your personal preferences, global rules, and the tooling that should follow you across every project.
2. **Project-specific setup**: the build commands, conventions, and architecture notes that live in a single repo.

The principle for both is the same: have one source of truth, and let each agent framework read from it.

## AGENTS.md is the standard now

The cross-framework standard for agent context is [`AGENTS.md`](https://agents.md/).
It is plain Markdown at the root of your repo, no schema required.

In December 2025 the [Agentic AI Foundation was announced under the Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-agentic-ai-foundation), co-founded by OpenAI (contributing `AGENTS.md`), Anthropic (contributing [MCP](https://modelcontextprotocol.io/)), and Block (contributing [goose](https://block.github.io/goose/)).
At the time of the announcement they reported over 60,000 open-source projects had already adopted `AGENTS.md`.

The big holdout is Claude Code, which still reads [`CLAUDE.md`](https://docs.anthropic.com/en/docs/claude-code/memory) instead.
The community workaround is a one-line `CLAUDE.md` containing `@AGENTS.md`, which uses Claude Code's [import syntax](https://docs.anthropic.com/en/docs/claude-code/memory#import-files) to pull in the same file.
The feature request is tracked at [anthropics/claude-code#6235](https://github.com/anthropics/claude-code/issues/6235).

## System-wide: one folder, many symlinks

For my personal global setup I want everything in a single git repo.
That way I can clone it on a new laptop and have all my agent configuration follow me.

The pattern that works is a canonical `~/agent-config/` directory, then symlink each tool's expected location at it.
Tools like [`ruler`](https://github.com/intellectronica/ruler) and [`aikado`](https://github.com/aikado/aikado) automate this.
[Rushi's symlink approach](https://rushi.dev/notes/agent-config-symlinks) is a good writeup of the manual version.

Roughly the layout looks like this:

```
~/agent-config/
├── AGENTS.md          # global context, loaded by everyone
├── rules/             # shared rules
├── skills/            # shared skills/commands
├── agents/            # shared subagent definitions
└── mcp/               # per-framework MCP configs (they can't be shared)
    ├── claude.mcp.json
    ├── codex.config.toml
    └── copilot.mcp.json
```

Then symlinks like:

```bash
ln -s ~/agent-config/AGENTS.md ~/.codex/AGENTS.md
ln -s ~/agent-config/AGENTS.md ~/.claude/CLAUDE.md
ln -s ~/agent-config/skills ~/.claude/skills
ln -s ~/agent-config/skills ~/.codex/skills
```

The whole `~/agent-config/` directory is a single git repo I push to a GitHub repository.
Clone it on a new machine, run a small `setup.sh` to create the symlinks, and every agent is configured.

One caveat: Codex uses [TOML for its config](https://github.com/openai/codex/blob/main/docs/config.md) and everyone else uses JSON.
You cannot symlink between them, so MCP servers end up as three hand-maintained files.

## Project-level: AGENTS.md at the root, then bridges

For a single project the pattern is simpler.

The setup I'm using on this blog and a few other repos:

- **`AGENTS.md`** at the root: the source of truth for project context, build commands, conventions, and "must follow" rules.
- **`CLAUDE.md`** as a one-liner with just `@AGENTS.md` inside.
- **`.github/copilot-instructions.md`** as a symlink to `../AGENTS.md` (or also a one-line file if you're on Windows).

That covers Claude Code, Codex, and Copilot with one editable file.

[Cursor](https://docs.cursor.com/context/rules) reads `AGENTS.md` natively as well.
[Windsurf](https://docs.windsurf.com/windsurf/cascade/memories#rules) does too.
[Aider](https://aider.chat/docs/config/aider_conf.html) needs `read: [AGENTS.md]` in `.aider.conf.yml`.

For monorepos, nested `AGENTS.md` files in subdirectories work in most readers, with the nearest file winning.
Codex walks down from the git root, Copilot's cloud agent picks the nearest, Cursor scopes subfolder rules.

## What does not transfer between tools

This is the part the marketing around `AGENTS.md` glosses over.
The shared file gets you context, and that is it.
Everything else is tool-specific:

- **MCP servers**: [Claude](https://docs.anthropic.com/en/docs/claude-code/mcp) uses `.mcp.json`, [Codex](https://github.com/openai/codex/blob/main/docs/config.md#mcp_servers) uses `[mcp_servers]` in `config.toml`, [Copilot in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) uses `.vscode/mcp.json` with `servers` (not `mcpServers`) as the top-level key. Three files, three formats.
- **Hooks**: Claude's [hook schema](https://docs.anthropic.com/en/docs/claude-code/hooks) lives in `settings.json` with 12+ event types. Codex has its own `hooks.json`. Copilot's cloud-agent equivalent is a [GitHub Actions workflow](https://docs.github.com/en/copilot/customizing-copilot/customizing-the-development-environment-for-copilot-coding-agent) at `.github/workflows/copilot-setup-steps.yml`. None of these are interchangeable.
- **Subagents**: Claude reads `.claude/agents/<name>.md`, Copilot reads `.github/agents/<name>.agent.md`, Codex defines them in TOML. The frontmatter shapes differ.
- **Slash commands and skills**: same story, different directories and different frontmatter.

For these, the realistic options are:

1. Maintain three copies by hand. Annoying but honest.
2. Keep one canonical `.agents/` directory in your repo and symlink each tool's directory at it. Breaks on Windows without `core.symlinks=true` and Developer Mode.
3. Use a generator (`ruler`, `aikado`, or a `make sync-agent-config` target) that writes the per-tool files from a single source. Treat the generated files as build artifacts.

I am leaning toward option 3 for anything beyond a single hobby repo.

## A precedence model worth documenting

One thing that helps once you have more than one agent and more than one repo is to write down which layer wins when configs conflict.

The model I use:

- **Layer 1: org policy**. Security rules, mandatory style, license headers. Distributed via [Claude managed settings](https://docs.anthropic.com/en/docs/claude-code/settings) or [Codex requirements.toml](https://github.com/openai/codex/blob/main/docs/config.md). Cannot be overridden.
- **Layer 2: repo conventions**. The `AGENTS.md` family. Tech stack, build commands, architectural patterns.
- **Layer 3: developer-local**. `CLAUDE.local.md`, personal Cursor rules, local Codex overrides. Never committed.

Writing this down in your root `AGENTS.md` saves a lot of "wait, which file overrides what" conversations later.

## What I would do today

If you are starting from zero and want a sensible setup in under an hour:

1. Create `AGENTS.md` at the repo root, keep it under 200 lines. Project description, stack, build/test/lint commands, must-follow rules.
2. Add a one-line `CLAUDE.md` with `@AGENTS.md`.
3. Symlink (or one-line) `.github/copilot-instructions.md` to `AGENTS.md`.
4. Accept that MCP, hooks, and subagents are separate files per tool, and only invest in a generator once you have three or more repos with the same setup.

The Anthropic side is likely to change.
A [Manifold market](https://manifold.markets/bessarabov/will-claude-code-support-agentsmd-i) puts the odds of Claude Code natively supporting `AGENTS.md` in 2026 at around 62%.
If that happens, the `CLAUDE.md` shim becomes unnecessary and the cross-tool story gets noticeably cleaner.

Until then, one `AGENTS.md` plus two thin bridges is the simplest thing that works.
