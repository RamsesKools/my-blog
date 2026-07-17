---
date: 2026-07-15
categories:
  - Tools
tags:
  - Tools
  - DevOps
---

# <img src="/assets/pre-commit.png" alt="pre-commit logo" style="height:1em; vertical-align:middle; display:inline;"> pre-commit

[pre-commit](https://pre-commit.com) is a framework for managing and running git hooks.

<!-- more -->

Define a `.pre-commit-config.yaml` in your repo and it will automatically run linters, formatters, and checks before every commit — across any programming language.

Consistency is key: the same checks run locally for every developer and in CI, with no manual setup beyond installing the hooks once (`pre-commit install`).
It creates value because it catches issues as easrly as possible: broken tests or missing commas are caugh before they ever hit a review or pipeline.

## Why I like it

[`pre-commit`](https://github.com/pre-commit/pre-commit) is a Python-native platform, and since I'm very familiar with Python it's a natural fit for me.
It's also a genuinely mature project: 117 releases, 138 contributors, and millions of users.

I use it as a general platform to run all sorts of checks and formatters, not just the obvious linting suspects.

### Teaching AI agents to use it

Besides that it is helpful for myself, I also found out that it is very helpful for my coding agents.
I explicitly prevent them from hand-formatting files or trying to fix every linter warning themselves.
Letting pre-commit's formatters and autofixers handle that instead saves a lot of tokens, and it's faster and more deterministic than an agent guessing at style.
That's why I make a point of teaching my AI coding agents to use pre-commit too.

## `pre-commit` in a CI pipeline

Because `pre-commit` comes with so many good checks out of the box, it makes sense to add these checks also to your CI pipleline.
We wouldn't ever want a broken `.yml` or `.json` file to be merged into our production code.

But, then why do we run these checks again after they should already have been run before every commmit?
Because, we can't **guarantee** that these checks have passed for each commit.
Another developer might not have run `pre-commit install` locally.
Or maybe I was doing a quick commit directly via [Github's web vscode editor](https://code.visualstudio.com/docs/remote/vscode-web) (this is a super cool feature btw, just press `.` on the keyboard from any repo and you will open it in a web-version of vscode).

## What's next

There's a Rust rewrite of pre-commit in the works: [prek](https://github.com/j178/prek).
I'm curious to see if it turns into the next `uv` or `ty` for this space, speeding up and improving my workflow the same way those did for Python tooling.
