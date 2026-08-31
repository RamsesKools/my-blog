---
date: 2026-08-28
slug: codeburn
tags:
  - Tools
  - AI
---

# <img src="/assets/codeburn.png" alt="CodeBurn logo" style="height:1em; vertical-align:middle; display:inline;"> CodeBurn

[CodeBurn](https://codeburn.app/) is a free and [open-source](https://github.com/getagentseal/codeburn) tool that helps me track how much tokens I burn during coding.
It is local and private: it reads the session files my AI coding tools already write to disk and shows my tokens actually go.
It runs as a terminal UI, a web view, or a MacOs menubar app.

<!-- more -->

## I was looking for a way to track token usage

My company gave me a limited AI budget: our GitHub Copilot license runs on metered "AI credits", and I was running out of credits consistently before the end of the month.
Separately, my own Claude Code usage kept bumping into session limits, and I felt I didn't know how to easily track this.

I wanted to know:

- What AI Coding sessions are using a lot of tokens?
- How can I optimize the tokens I'm using?
- Am I going to run out of quota before the end of the 5 hour session / week / month?

I specificaly hoped to find one tool that can be used for multiple coding agent harnasses: Claude Code, Github Copilot, and Codex.
I made a list of promising tools, but only [ccusage](https://ccusage.com/) and Codeburn really stood out.
CodeBurn was the first one on my list to try, because it looked the most feature-complete for what I needed, and because it looked really cool!

I'm very happy with it since I started using it about a month ago.

## How I use it

I installed it globally with npmm, then installing the MacOs menubar was just a cli command.
The `codeburn` CLI is great for taking a closer look, especially if I want to optimize my token usage.

But the menubar is the feature I use the most.
Seeing the euro counter tick up in the menubar all day turns out to be the best part.
It is a constant, gentle reminder to spend tokens deliberately.

## What it showed me

The `optimize` scan was the immediate win.
It flagged two MCP servers that were silently burning tokens on every session, neither of which I had installed on purpose:

- A GitKraken MCP server, added automatically by the VS Code GitLens extension.
- A Gmail MCP server that Claude installed on my machine because I once clicked the Gmail/Calendar plugin on the claude.ai website.

I really dislike this pattern where tools are silently installing MCP servers.
A tool should not quietly install an MCP server on my machine because I clicked something once in a browser.

Beyond that it gave me the insights I was missing: cost per session, cache hit rate, and which skills I lean on most.
The part I did not know I need was: `codeburn plan set claude-pro`
It [tracks my Claude plan](https://codeburn.app/docs/plans) and estimates whether I will hit 100% usage before the reset timer, which is amazing.

## What I do not use, yet

I do not really use the "yield" metric that correlates spend with git commits as productive, reverted, or abandoned.
I still review every commit myself, so I already know whether one was worth it.

What I would find valuable is token cost per PR opened or per issue closed.
That needs my agentic flow to get more autonomous first, so agents can work longer and finish whole tickets on their own.
I think I am slowly getting there, though I am a little afraid my token budget will not stretch to fully automating my work: some tasks still need a lot of steering when I use a cheaper model.

## One thing I'm still missing

It tracks Claude Code and GitHub Copilot for me today, and I will add Codex once I use it more.

A feature that I hope the Codeburn developers will still implement: tracking of monthly Github Copilot AI Credits.
I [opened an issue](https://github.com/getagentseal/codeburn/issues/943) about 3 weeks ago, and today I saw that it was already implemented
Unfortunately, it isn't working for my Github Copilot Business plan, and I've created two follow-up issues for it.
But the fact that the Codeburn developers pick up this work so fast is amazing to see nonetheless, and gives me high hopes for the future of this tool!
