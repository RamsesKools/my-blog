---
date: 2026-11-02
slug: ai-assisted-programming
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
This gave me a glimpse into the future where AI would slowly take over writing of the code.

## Chat: ChatGPT

When [ChatGPT came out in November 2022](https://chatgpt.com/) I started dropping error logs and code snippets into it.
It was basically a chat assistant, and I was manually bringing in all the context each time.
I started briging in more and more context, until I was struggling to keep the model performant.
In the end I mostly used it as a better Google or Stack Overflow.

## Agentic coding: Claude Code

Then [Claude Code arrived in February 2025](https://www.anthropic.com/news/claude-3-7-sonnet), and WOW I was amazed!
Finally the agent could gather its own context and write and update files itself.
At first I worked very carefully: manually approving everything, and still understanding every line of code.

I got used to it quickly.
I also started using AI to learn new things a lot faster: AWS CDK, TypeScript, SQL, Bicep, Terraform, Docker, and front-end work with HTML, CSS, JavaScript and React.

## A hub in VS Code

Next I embedded Claude Code completely in VS Code.
I built a custom hub workspace with multiple repos, git-versioned docs, skills, and context files (see [[agent-config|how I configure my agents once]]).
From there I could quickly find what I was looking for across repos, and order agents around in all of them.

I built custom skills and workflows on top, like my [[ai-agents-data-analysis|data analysis workflow]].
But also skills that teach my agents specific workflows or how to connect with my services (such as Jira and Confluence).

Honestly, I still like this way of working.
It allows me to stay in control of the code and I can quickly go through my codebase.
However, managing worktrees, multiple agents and sessions gets overwhelming, and finding that one session again is hard.

## Captain and crew: Orca

So I wanted to try to go more hands-off, and coordinate multiple agent sessions from one captain.
That's where [[orca|Orca]] came in for me.

My setup and workflow looks as follows:

- I still use a hub repo that manages my projects: I store workflows, tickets and docs here.
- From my hub repo I run a coordinator agent session: it plans, creates GitHub issues, and reviews and merges PRs, but does no real work itself.
- All work is described in issues that agents can pick up: refinement, prototyping, and implementation issues.
- For each issue, the hub starts a worker in a new Orca workspace with its own branch, linked to that issue, and a self-contained starter prompt.
- I instruct my 'captain' to push forward the agents with their implementation until they produce a PR that is ready for my review.

## Where this is going

Looking back, every step forward came down to managing context more efficiently.
With ChatGPT I pasted it in by hand, Claude Code went and found it on its own, and my hub and skills exist to give my agents easier access to the relevant context.

The hands-off approach works really well for my smaller hobby projects.
The enterprise projects at work are harder: they need more context and more specific tools, and my agents have a tougher time finding their way around.
So while I still work closely alongside my coding agents, I will put great effort into making those projects easier for agents to understand.

It's early, but I'm pretty sure this is the future: me writing less code and managing more of the agents that write it.
Models, harnesses, MCP servers and skills will keep getting better, and the better my projects' context gets, the more I can hand over.
With time the size of the problems my agents can tackle succesfully will keep increasing.
I think at some point I will only be needed to choose the direction the codebase takes and the high-level decisions about the work.
