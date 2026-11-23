---
date: 2026-11-02
slug: ai-assisted-programming
tags:
  - AI
---

# My journey into AI-assisted programming

Since the arrival of GH Copilot and ChatGPT, I quickly started using it to help with programming.
Now, 4 years later, the available tools have been improved over and over again, and I keep trying to follow along.
In this article I tell a little bit about that journey.

<!-- more -->

## Before AI

During my studies I learned how to program: C first, then Python, then C++.
I started writing it all in Vim, Sublime Text and Code::Blocks.
Those early years were a lot of:

- Struggling to find answers to niche issues on Stack Overflow and other forums.
- Monkey-see-monkey-do: copying patterns from others and making small adjustments.
- Debugging with print statements.

My first job as 'Decision Support Consultant' got me building C++ revenue management software, which was customized and deployed for each customer.
That meant lots of niche, custom C++ engineering, including a wxWidgets front-end.
I got really good with the Visual Studio debugger there, while VS Code slowly took over everything that wasn't C++.
We were not (yet) using a proper testing framework or code pipelines, and deploying was done via remote desktop and copying files.

Then I became a 'Big Data Engineer' at a Dutch consultancy firm.
My first project, at KLM, took my C++ and Python a lot deeper.
I worked with Boost, upgraded C++ versions, debugged makefiles, moved the build to CMake, built Python packages with pybind11, and containerized a C++ app.
I also learned a lot about DevOps, deploying a first app to Azure and configuring and setting up a build + test server in TeamCity.

After that my work gradually shifted toward cloud, data and AI.
In this time I expanded my 'tech-stack' with all sorts of new tools:

- Cloud: AWS and Azure.
- Databases: Postgres, Redshift, Athena and Databricks.
- CI/CD: TeamCity, Bamboo and GitHub Actions.
- Infra as Code: Terraform, Bicep and AWS CDK.
- Python tooling: poetry, uv, pytest, flake8, mypy, black, isort, ruff and ty.

Along the way VS Code became my workspace of choice, packed with extensions I kept tweaking.

## Autocomplete: GitHub Copilot

I started programming with AI when [GitHub Copilot launched in June 2021](https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/).
At first it was just a smarter autocomplete.
But then, with multi-line autocomplete, the AI could sometimes fill in whole classes or functions.
AI was starting to make typing code easier, but not much more yet.

## Chat: ChatGPT

When [ChatGPT came out in November 2022](https://openai.com/index/chatgpt/) I started dropping error logs and code snippets into it.
It was basically a chat assistant, and I was manually bringing in all the context each time.
I kept adding more and more context, until the model started struggling under it.
I could use it to quickly get answers to simple questions, and even on more complex problems it could often help me structure the problem and steer me in the right direction.

## Agentic coding: Claude Code

Then [Claude Code arrived in February 2025](https://www.anthropic.com/news/claude-3-7-sonnet), and **WOW**.
Finally the agent could gather its own context and write and update files itself.
No more copy+paste from and to the chat window!
At first I worked very carefully: manually approving all commands and checking all file edits.
I was checking all diffs before each commit, and often fixing small issues.

But as AI models got better and my workflow improved, I noticed that my checks were not really necessary anymore and were just slowing down the development.

## A hub in VS Code

Now I've built a custom hub workspace with multiple repos, git-versioned docs, skills, and other agent configuration (see [[agent-config|how I configure my agents once]]).
From there I can quickly find what I was looking for across repos, and order agents around in all of them.

I built custom skills and workflows on top, like my [[ai-agents-data-analysis|data analysis workflow]], plus skills that connect my agents to services like Jira and Confluence.

I still like this way of working.
I stay in control of the code and can quickly move through my codebase.
But managing worktrees, multiple agents and sessions gets overwhelming, and finding that one session again in VS Code is hard.

## Multi-agent programming: Orca

Since models and harnesses were getting more capable, I wanted to go more hands-off, and coordinate multiple agent sessions at once.
That's where [[orca|Orca]] came in for me.

My setup:

- I still use a hub repo that manages my projects: I store workflows, tickets and docs here.
- From the hub I run a coordinator agent: it plans, creates GitHub issues, and reviews and merges PRs, but does no real work itself.
- All work is described in issues that agents can pick up: refinement, prototyping, and implementation issues.
- For each issue, the coordinator starts a worker in a new Orca workspace with its own branch, linked to that issue, and a self-contained starter prompt.
- I try to set up the workflow in such a way that the agents can focus on creating PRs that are tested and ready for me to review.
- Complex multi-session work that can't be completed in one session is tackled via an approach called [`/wayfinder`](https://www.aihero.dev/skills-wayfinder)
- I've built a custom modification to this skill and a tool to visualize the `wayfinder-map` beautifully: <https://github.com/RamsesKools/wayfinder-maps>


## Where this is going

I will keep automating my own job, now it is just through the use of AI agents instead of handwritten scripts.
I still really enjoy my work, now I finally feel like a '10x engineer', and I'm getting more done than ever; or maybe I'm just feeling like I'm getting a lot done, because so much text is generated on my screen?

I do think that:

- Writing code becomes less about the code itself, and more about defining what the code needs to do accurately and creating a framework to test whether the code is behaving correctly.
- AI agents can produce code so fast that human engineers will quickly become the bottleneck if we try to read and verify each line.
- To verify AI agents quickly at a glance, it helps to make things visual: progress, proof of work, simple indicators.
- The output of AI agents will get trusted more and more.
