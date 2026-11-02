---
date: 2026-11-02
slug: ai-assisted-programming
draft: true
tags:
  - AI
---

# My journey into AI-assisted programming

I went from copying patterns off Stack Overflow, to tab-completing with Copilot, to pasting error logs into ChatGPT, to a coordinator agent coordinating a crew of workers.
Every step handed a bit more of the work to the machine, and moved me a bit further away from the code.
Here's how that went.

<!-- more -->

## Before AI

During my studies I learned C first, then Python, then C++, writing it all in Vim, Sublime Text and Code::Blocks.
Those early years were a lot of:

- Struggling to find answers to niche issues on Stack Overflow and other forums.
- Monkey-see-monkey-do: copying patterns from others without fully getting them.
- Debugging with print statements.

My first job was in-house, building our C++ decision support software, which we customized and deployed for each customer.
That meant lots of niche, custom C++ engineering, including a wxWidgets front-end.
I got really good with the Visual Studio debugger there, while VS Code slowly took over everything that wasn't C++.

Then I became a Big Data Engineer at a consultancy.
My first stint, at KLM, took my C++ and Python a lot deeper.
I worked with Boost, upgraded C++ versions, debugged makefiles, moved the build to CMake, built Python packages with pybind11, and containerized a C++ app.

After that my work gradually shifted to cloud and data:

- Cloud: AWS and Azure.
- Databases: Postgres, Redshift, Athena and Databricks.
- CI/CD: TeamCity, Bamboo and GitHub Actions.
- Python tooling: poetry, uv, pytest, flake8, mypy, black, isort, ruff and ty.

Along the way VS Code became my home base, packed with extensions I kept tweaking.

## Autocomplete: GitHub Copilot

I started programming with AI when [GitHub Copilot launched in June 2021](https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/).
At first it was just a smarter autocomplete.
Then I saw people trying to hand over more of the programming to it: write a description of a function or class, let the autocomplete fill it in, then hand-tune the rest.

## Chat: ChatGPT

When [ChatGPT came out in November 2022](https://openai.com/index/chatgpt/) I started dropping error logs and code snippets into it.
It was basically a chat assistant, and I was manually bringing in all the valuable context.
More and more context, actually, until I was struggling to keep the model performant.
In the end I mostly used it as a better Google or Stack Overflow.

## Agents: Claude Code

Then [Claude Code arrived in February 2025](https://www.anthropic.com/news/claude-3-7-sonnet), and WOW.
Finally the agent could gather its own context and write and update files itself.
At first I worked very carefully: manually approving everything, and still understanding every line of code.

I got used to it quickly.
I also started using AI to learn new things a lot faster: AWS CDK, TypeScript, SQL, Bicep, Terraform, Docker, and front-end work with HTML, CSS, JavaScript and React.

## A hub in VS Code

Next I embedded Claude Code completely in VS Code.
I built a custom hub workspace with multiple repos, git-versioned docs, skills, and context files (see [[agent-config|how I configure my agents once]]).
From there I could quickly find what I was looking for across repos, and order agents around in all of them.

I built custom skills and workflows on top, like my [[ai-agents-data-analysis|data analysis workflow]].
That one only really works properly in VS Code with the native GitHub Copilot extension, or through a Jupyter MCP server.

Honestly, I still like this way of working.
But it stays very close to the code.
Managing worktrees, multiple agents and sessions gets overwhelming, and finding that one session again is hard.

## Captain and crew: Orca

So I wanted to go more hands-off, and coordinate multiple agent sessions from one captain.
That's where [[orca|Orca]] comes in.

My setup lives in my agents config repo:

- The repo's main workspace is the hub: it plans, creates GitHub issues, and reviews and merges PRs, but does no real work itself.
- For each issue, the hub starts a worker in a new Orca workspace with its own branch, linked to that issue, and a self-contained starter prompt.
- A small dispatcher script polls the Orca workflow board and runs reviewer and fixer agents in a loop, until the PR is clean or ready for human review.

That dispatcher is plain bash, not an agent, so it costs no tokens.
It's also my workaround for Orca not triggering on board changes itself yet.
