---
date: 2026-10-30
slug: orca
draft: true
tags:
  - Tools
  - AI
---

# Orca

[Orca](https://onorca.dev/) is an Agent Development Environment (ADE): a desktop app where you run, track, and coordinate a bunch of coding agents in parallel, each in its own workspace and git worktree.
It works with whatever agent harness you like (Claude Code, Codex, Copilot CLI, and more), and that's what sold me.

<!-- more -->

I've only used Orca for about 3 weeks, so take this as a first impression.
For how I ended up here, see [[ai-assisted-programming|my journey into AI-assisted programming]].

## Why I went looking

The better I got at working with coding agents, the longer they could run on their own.
So I stepped back and micro-managed a lot less, which brought a new set of problems:

- Juggling agents across a pile of CLI and VS Code windows got really hard.
- I kept losing track of the sessions that mattered.
- I had to build my own skills and hooks just to get notified (see [[peon-ping]]).
- Configuring and orchestrating agents across harnesses takes a lot of work (see [[agent-config|how I configure my agents once]]). It still does.

I want to stay harness- and modelprovider-agnostic, so Claude Desktop and Codex Desktop weren't for me, even though they're nice ADEs.
Claude Code's `/remote-control` is great too, but it only covers Claude.

Honestly, I still love VS Code for when I want to inspect every diff no every file and work directly on the code myself.
But with Orca I've found the tool that allows me to step back and become a manager of agents.

## What I love about it

- Workspaces make parallel worktrees easy, and I keep a nice overview of all of them.
    - Creating git worktrees manually just gave a bit too much friction.
    - I also tried the cli-native approach via [`treehouse`](https://github.com/kunchenguid/treehouse).
- A global session finder, so I stop losing that one session that had all the context.
- My agents use the `orca` CLI to manage other agents, and they're efficient at it.
    - `orca` cli allows an agent to quickly create a new workspace+worktree (in another repo if needed).
- Agents message each other through inboxes, which makes working together smooth. It feels really good to let one captain agent coordinate a few workers, an idea I took from Kun Chen's [firstmate](https://github.com/kunchenguid/firstmate), where a first mate spawns and supervises a crew of agents.
- The Jira and GitHub integrations are really nice (Linear too, but I don't use it).
- The mobile app was easy to set up, and now I can follow all my agents and terminals from my phone. Phone notifications were a breeze too!

## What I hope they improve

- More granular notifications, since right now it's mostly all or nothing.
- Config as code. I'd love to define more things in files, Orca Automations for example.
- Automations that run a script. Not every automation needs an agent.
- Ticket status that triggers agents, so a PR marked ready for review gets picked up by a reviewer agent automatically.
- A workflow board that ties it all together. I like the idea of the board, but a status per workspace doesn't quite make sense to me. What I'd love:
    1. A Jira, GitHub, Linear, or manual ticket is created and tied to a workspace.
    2. That ticket moves through stages I configure myself, in code or config files.
    3. Workspaces and sessions start, hand over, and coordinate based on the ticket's stage.

Right now the board and the ticket don't feel connected.
Or I just don't get it yet, three weeks in.
