---
date: 2026-06-01
draft: true
---

# How to configure all your AI-Agents once

*Dealing with different agent frameworks and staying coding agent framework agnostic.*

I switch between [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://github.com/openai/codex), and [GitHub Copilot](https://github.com/features/copilot) depending on the project.
Each one wants its own config files in its own place, in its own format.
This post is about how to personalize all your AI-Agents in one place.

<!-- more -->

## What the hell am I talking about? AI-Agents what?

<!-- TODO CHECK THIS section writing here before publishing.-->

> Let me first briefly introduce the concepts of LLMs, AI-Agents, and AI-Assisted programming.

I've been using LLM-based AI tools since ChatGPT first became popular in 2023.
This started out with me writing and copy+pasting questions or problems into ChatGPT.
Despite many problems, this was still an amazingly helpful tool.

Since Github Copilot came out I've been keeping track of IDE extensions that let you bring the AI tool directly into your PC.
Since Anthorpic came with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) I have really kicked off my journey with AI-assisted programming.
Claude Code runs directly on your computer, can read your files and use your tools.
You can build a script, run it, debug it, test it, all just by instructing Claude Code to do so in the language for your choice.

ChatGPT already showed that modifying the system prompt can save you a lot of time and helps with customzing the behavior of the model.
Now with the new models, MCP servers, and agent skills it is even more powerfull and more important to keep track of the instructions and context.
MCP servers can help you connect your AI-system to other systems, and skills can teach your model to use these MCP server and other tools.

Even though I think Claude Code was the first tool that worked really well and showed me the power of AI-assisted programming, nowadays there are multiple different AI that all do basically the same thing.
Just to name the other 3 most popular AI-Assisted coding tools: Github Copilot, ChatGPT Codex, and Cursor.
At the moment I'm actively using 3 of these tools: I have a personal Anthropic subscription for Claude Code, a Github Copilot license and a ChatGPT Enterprise Codex license through the company I'm working for.

All of these tools are really powerfull, especially when given the right context and instructed in the correct way.

## Two places where we customize AI-agent behavior locally

I configure and setup my AI-Agents in two places:

1. **System-wide setup**: my personal preferences, global rules, and the tooling that should follow me across every project.
2. **Project-specific setup**: the build commands, conventions, and architecture notes that live in a single repo.

The principle for both is the same: have one source of truth, and let each agent framework read from it.
Additionally, I want to store the configuration in a git-repository, which allows me to version it, and also let's me use the same configuration easily on multiple devices.

## The different types of customization and context

### Context via `AGENTS.md` or `CLAUDE.md`

Just a small markdown file with some additional context to enhance the system prompt for each chat: `AGENTS.md`, `CLAUDE.md`, `copilot-instructions.md` 
  
  We should try to keep these small, since they will always be loaded.

### Skills

<!--TODO How is this different from COMMANDS? comment on that.-->

Skills are essentially just markdown files teaching the AI-Agent to do a specific task.
Each AI-agent framework have their own way to detect and trigger when a skill should be used.
Since skills are just markdown files, they can be used be any AI-agent framework.
While this might seem simple, it is really powerfull if used correctly.

One thing that can be very powerfull is to combine a skill with a CLI application.
For example, the github cli tool `gh` combined with it's skills allows your AI-agent to interact with everything in your github repository: commits, branches, pull-requests, issues, github actions workflow runs, and more.

### Plugins or extensions

These are still an emerging concept, but in essence this is a combination of tools, skills, agents, hooks, and mcp servers that together add specific functionalities on one topic.
For example, you can have a plugin for interacting with excel files, or a plugin for interacting with Google Calendar.

<!--Add links to Claude code market place, plugin documentation and Codex/copilot plugin support/documentation-->

At the moment Claude Code is leading with this and they have a decently mature plugin marketplace. Besides that Codex is starting to do the same and they are compatible with Claude Code's market place. Github Copilot has extensions which try to do the same thing, but in a slightly different way, and therefore this is not really compatible with the plugin ecosystem of Claude.

### Agents and subagents

These can be seen as personas for your AI-agent framework.
They allow you to

- Set a custom system prompt.
- Customize which model is used and 'how hard it thinks'.
- Customize what tools, skills and MCP-servers it can use, and which it can't use.

An example agent can be a code-reviewer agent, which you can set to only have read-access to files and for example allow it to write commands on a pull-request.
Agents and subagents become really powerfull when you allow one agent to offload work to another **subagent**.
For example, when you write code, you can use a powerfull model (for example: Claude Opus 4.8) to implement a feature, and then instruct it to use a sub-agent that uses a smaller model (for example: Claude Haiku 4.5) to fix linting and formatting issues.
This can really help to keep 

### Hooks

<!--TODO -->

> Hooks allow you to execute custom shell commands at key points during agent execution, enabling you to add validation, logging, security scanning, or workflow automation.

But to be honest, I'm not yet really using hooks, so I can't say much more about it then mention what they are.

### Framework settings

<!--TODO write briefly what settings are-->

- Each framework can be configured with settings.
  - Allow/disallow access to files and tools.
  - Configure mcp server
  - Configure access to plugin marketplace
  - 

## AGENTS.md is the standard now

The cross-framework standard for agent context is [`AGENTS.md`](https://agents.md/).
It is plain Markdown at the root of your repo, no schema required.

In December 2025 the [Agentic AI Foundation was announced under the Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-agentic-ai-foundation), co-founded by OpenAI (contributing `AGENTS.md`), Anthropic (contributing [MCP](https://modelcontextprotocol.io/)), and Block (contributing [goose](https://block.github.io/goose/)).
They report that over 60,000 open-source projects have already adopted `AGENTS.md`.

The big holdout is Claude Code, which still reads [`CLAUDE.md`](https://docs.anthropic.com/en/docs/claude-code/memory) instead.
The community workaround is a one-line `CLAUDE.md` containing `@AGENTS.md`, which uses Claude Code's [import syntax](https://docs.anthropic.com/en/docs/claude-code/memory#import-files) to pull in the same file.
The feature request is tracked at [anthropics/claude-code#6235](https://github.com/anthropics/claude-code/issues/6235).

## System-wide AI-Agent configuration: one folder, many symlinks

I clone my personal agent config git repo to the central `~/agent-config/` directory, then use symlinks to make each tools expected files available for them in their expected location.

<!--TODO link my github ai agent config repo and improve this writing -->

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

After cloning this repo on a new machine, I run a small `setup.sh` to create the symlinks, and every agent is configured.

There are offcourse some caveats, not all the configuration is uniform, so I still need to maintain separate config files also.
For example: Codex uses [TOML for its config](https://github.com/openai/codex/blob/main/docs/config.md) and everyone else uses JSON.
That is why for example MCP servers, and framework settings, end up as three hand-maintained files.

## Project-level: AGENTS.md at the root, then bridges

For a single project the pattern is simpler.

The setup I'm using on this blog and a few other repos:

- **`AGENTS.md`** at the root: the source of truth for project context, build commands, conventions, and "must follow" rules.
  - This can be used by Github Copilot and Codex automatically when placed in the correct locations.
  - For Claude Code we have rename the file to `CLAUDE.md` when symlinking it, or we create a `CLAUDE.md` file with `@AGENTS.md` locally.

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

<!-- TODO rewrite this after making up my mind on what AI-agent config I want  -->

## What I would do today

If you are starting from zero and want a sensible setup in under an hour:

1. Create `AGENTS.md` at the repo root, keep it under 200 lines. Project description, stack, build/test/lint commands, must-follow rules.
    - Only put things in here that are **always** how you want to work with you AI-agent.
    - For example: preferred agent behavior, writing style, information about who you are and what you do, and your other general preferences.
2. Add a one-line `CLAUDE.md` with `@AGENTS.md`.
3. Symlink (or one-line) `.github/copilot-instructions.md` to `AGENTS.md`.
4. Accept that MCP, hooks, and subagents are separate files per tool, and only invest in a generator once you have three or more repos with the same setup.

The Anthropic side is likely to change.
A [Manifold market](https://manifold.markets/bessarabov/will-claude-code-support-agentsmd-i) puts the odds of Claude Code natively supporting `AGENTS.md` in 2026 at around 62%.
If that happens, the `CLAUDE.md` shim becomes unnecessary and the cross-tool story gets noticeably cleaner.

Until then, one `AGENTS.md` plus two thin bridges is the simplest thing that works.
