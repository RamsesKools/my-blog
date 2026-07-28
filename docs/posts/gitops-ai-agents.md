---
date: 2026-07-28
slug: gitops-ai-agents
tags:
  - DevOps
  - AI
  - Infra
---

# Using GitOps to empower your AI agents

AI coding agents can write code quickly, but writing code is rarely the hard part.
To make a useful change, an agent needs to understand how your application is built, configured, tested, deployed, and operated.
If that knowledge is scattered across cloud portals, wikis, and people's heads, the agent is working with only part of the picture.

This is where GitOps gives us an advantage.
The same practices that make systems reproducible and easier for engineers to operate also make them legible and actionable for agents.

<!-- more -->

I'll first unpack the GitOps and DevOps concepts behind that idea, then walk through a Python-heavy monorepo example before showing how it all comes together in agentic coding.

## What is GitOps

[GitOps](https://opengitops.dev/) is what you get when you combine DevOps principles with Git as the single source of truth.
Instead of clicking through a cloud console or SSH-ing into a server to make a change, you commit it: your application code, your infrastructure definitions, and your configuration all live as code, in the same version control system, going through the same review process.
Git becomes the one place that describes the desired state of everything, and automation reconciles reality to match it.

## DevOps vs GitOps

They get used interchangeably, but they're not quite the same thing.
DevOps is the broader culture: breaking down the wall between development and operations, shared ownership, fast feedback loops.
It doesn't prescribe a specific mechanism for getting there.
GitOps is one specific way of practicing that culture: Git becomes the single source of truth for your desired state, and automation continuously reconciles reality to match it.
Every GitOps setup is a form of DevOps.
Not every DevOps setup is strictly GitOps: a pipeline that pushes changes out by hand is still very "DevOps," even without Git driving the reconciliation.

## DevOps automation

GitOps only pays off when the automation underneath it is actually set up well.
The pattern that works best for me has three stages:

1. **Pre-commit, locally.** Fast checks (linting, formatting) run on your machine before a commit even lands, so you catch the trivial stuff instantly instead of waiting on a pipeline.
2. **CI, on every PR.** The full test and validation suite runs on every commit pushed to a pull request.
3. **CD, after merge.** Once a PR lands on the main branch, deployment happens automatically.

Together, these stages give an agent a machine-readable definition of done: local checks for fast feedback, CI for full validation, and CD for delivery.
This blog is a small example of exactly that pattern: [[blog-infrastructure|CI/CD via GitHub Actions and a Dagu preview pipeline]] runs on every push and release.

## GitOps in practice

If DevOps is the culture, GitOps in practice means actually using tools to configure every aspect of your app, data, infra, and docs as code.
GitOps does not require a monorepo, but that is the example I focus on here because it makes the argument strongest: bringing context, configuration, documentation, and application logic together makes the complete system more accessible to both engineers and agents.

- **Docs as code.** Markdown (or similar) committed alongside the code, built into a human-readable site and deployed somewhere people can actually read it: [[blog-infrastructure|this blog is that pattern]].
  Keeping troubleshooting notes, how-tos, presentations, and diagrams in a separate wiki or drive creates two problems: you have to remember to update them separately every time the code changes, and it puts a wall between your docs and any AI agent working from the repo.
  It can't read what it can't see.
- **Infrastructure as code.** [Terraform](https://www.terraform.io/), [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview), or [AWS CDK](https://aws.amazon.com/cdk/): whichever fits your cloud and the level of abstraction you want, defined and reviewed the same way as application code.
- **A `Dockerfile` for the runtime environment.** The environment your code actually runs in is itself declared and versioned, not hand-configured on a server.
- **Multiple environments via parameters, not branches.** Dev/ACC/PRD should be the same code with different parameters or variables, not long-lived environment branches that quietly drift apart from each other.
- **Data as code.** A framework that lets you define transformations, tests, and documentation for your data models as code: [dbt](https://www.getdbt.com/) is my go-to here.
- **Pipeline definitions as code.** The CI/CD workflows themselves live in the repo, versioned like everything else.
- **Observability as code.** Dashboards and alert rules defined as code rather than clicked together in a UI, so they survive and travel with the system they monitor.

## Repo structure for a data product

Not every repo is a single Python package.
The architecture below is specifically a Python-heavy data product with dbt transformations and infrastructure as code, because that is a kind of project I am comfortable building.
It has several pieces that evolve somewhat independently but still need to ship together: a shared library, a data ingestion pipeline, a back-end, and a front-end.

[uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) handle exactly this: one repo, one lockfile, multiple Python projects as workspace members that can depend on each other without being published anywhere.
In practice that means a shared library member other components import, a data-ingestion member, a back-end member, and a front-end member, all resolved and locked together.
You can genuinely do anything with Python across the stack and still get one coherent dependency graph.

Everything else in the repo follows the same "one source of truth" idea: `infra/` for the Terraform/Bicep/CDK definitions, `docs/` for the MkDocs site, `notebooks/` for exploratory work, and `dbt/` for the data transformations and their generated documentation.
Keeping tests and documentation in the same repo with the code they cover is a strong preference and recommendation of mine.

![GitOps monorepo and runtime architecture for a Python-heavy data + AI product using dbt and infrastructure as code](/assets/gitops-ai-agents-architecture.png)

## GitOps and agentic coding

When you run a coding agent ([Claude Code](https://code.claude.com/docs/en/overview), [GitHub Copilot](https://docs.github.com/en/copilot), [Codex](https://developers.openai.com/codex/cli/), [OpenCode](https://opencode.ai/), or others) from your local IDE, it can inspect the repository and the development environment it has access to while building features or solving problems.
Ask it to build a new feature and it will draft a plan, then investigate your files to figure out your repo's setup, its existing packages, and its conventions, before writing a single line.
That works best exactly when the repo gives it a complete picture: infra, config, and code all in one place, nothing hidden behind a console or a wiki it can't reach.

Agents work even better when they can programmatically interact with your infra, not just read about it.
CLI tools like `gh`, `aws`, `az`, `terraform`, and `bicep` (a few I like, though there are plenty more) let an agent act on infra directly instead of just describing what you should click.
The `az` CLI in particular has been working wonderfully for a project I'm on right now.
After I authenticate with `az login`, I can give my agents access to the Azure environment relatively easily.
They can use the CLI for most of the same tasks I would perform in the portal, such as reading logs, starting containers, or inspecting infrastructure configuration.
Besides operating the cloud infrastructure, this also helps agents verify whether the deployed state still matches the code.
That difference is known as infrastructure drift, and it can become a serious problem when changes made outside Git go unnoticed.

The other route in is MCP servers: more cloud and software platforms are shipping them, including project management tools like Linear, GitHub, Jira, and Confluence.

## Teaching your agents

The real multiplier kicks in once you teach your agents through custom skills, `AGENTS.md`, or plain Markdown documentation, rather than repeating yourself in every session.
GitOps makes the system visible and reproducible, agent instructions explain how your team expects that system to be changed, and tools give agents controlled ways to act on it.

- **Preferences, at two layers.** Global preferences (how you like to work, in general) and repo preferences (how this project specifically works) are different things, and keeping them separate matters.
  See [[agent-config|how I set this up once, globally and per repo]].
- **Teach the repo, not just the task.** Documenting where to look for what saves a lot of tokens, because the agent's investigation gets a lot more focused instead of re-discovering your conventions from scratch every session.
- **Teach infra interaction.** Whether that's MCP servers or CLI tools, spell out how the agent should touch your infra rather than letting it guess.
- **When docs get vast, teach search.** Once documentation grows past what fits in context, [[qmd|QMD]] gives an agent semantic search over it instead of blind grepping.
- **Teach the whole workflow.** Read the ticket (a GitHub issue, an ADO or Jira user story) → draft a plan and track it on the ticket → start a branch (in a new worktree/workspace if you want to build in parallel) → write the code → format and lint through your tooling, not by manually chasing linter output → write and run tests → open a PR → check the CI result → update the ticket or send a notification about the review request.
  Go all-in on agentic, and a second agent spins up to review that PR and suggest follow-up work.

## Where this is headed

This agentic coding technology is so new, and moving so quickly, that I don't think there's one "best" way of working with it yet.
I need to experiment more, and the tools themselves keep changing under my feet.
New ones show up constantly.

My bet: the GitOps and DevOps practices that were already worth having before agentic coding existed are only going to matter more, not less.
The more disciplined your repo already is, the more of that discipline an agent can pick up and run with.
