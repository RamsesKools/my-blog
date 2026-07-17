---
date: 2026-07-15
tags:
  - Tools
---

# <img src="/assets/uv.png" alt="uv logo" style="height:1em; vertical-align:middle; display:inline;"> uv

[uv](https://docs.astral.sh/uv/) is a Python package and project manager written in Rust, built by [Astral](https://astral.sh).
It's a fairly new project, only public since 2024, but it's already become a sort-of successor to [Poetry](https://python-poetry.org).

<!-- more -->

It replaces `pip`, `pip-tools`, `pipx`, `virtualenv`, `pyenv`, and parts of `poetry` — all in one tool, and drastically faster.

## How I got here

My relationship with Python dependency management has been a slow accumulation of lessons learned the hard way.

It started with small scripts written in a highschool computer class, no packaging involved at all.
At university I picked Python back up for data analysis and visualization, a natural fit alongside my computational chemistry studies.
That's when I first ran into environments: I learned that a `.venv` is crucial, because without one every package you install lands in the same global environment.
Work on more than one project at a time and that becomes a real problem fast.

Next came `requirements.txt`, which mattered as soon as I needed to bring my environment to another machine.
Then I learned why locking versions matters, the hard way: I installed an old `requirements.txt`, it happily pulled in the latest version of everything, and my code stopped working.

When I started at Future Facts I dove into Python more seriously and realized that locking every dependency version by hand is tedious and error-prone at any real scale.
That's when I discovered Poetry and `pyproject.toml`, and I embraced it.
Around the same time I learned to manage different Python versions with [pyenv](https://github.com/pyenv/pyenv).
This matters because different projects often want or require different Python versions, and juggling multiple executables and versions in your PATH by hand is tedious.
pyenv makes it a non-issue.
On Windows pyenv itself doesn't exist, but [pyenv-win](https://github.com/pyenv-win/pyenv-win) is a decent replacement.

## Why I moved from Poetry to uv

This year I moved from Poetry to uv.

The first thing you notice is speed: dependency resolution and installs that took Poetry seconds to tens of seconds finish almost instantly with uv.
It also manages Python versions itself, so pyenv is no longer needed either.
`uv python install 3.12` and a `.python-version` file are enough, and `uv run` will fetch and use the right interpreter automatically.

A few other things it does that Poetry doesn't:

- `uvx` runs a tool in an ephemeral, isolated environment without installing it first, similar to `pipx run` but built in.
- It supports inline script dependencies ([PEP 723](https://peps.python.org/pep-0723/)), so a single-file script can declare its own dependencies in a comment header.
  `uv run script.py` just works, no project or virtualenv setup needed.
- It ships as a single static binary, so bootstrapping it doesn't itself depend on having a working Python installation.

What I like most about it: it just works.
Drop in a `pyproject.toml`, run `uv sync`, and you have a reproducible environment in seconds.
No fussing with virtualenvs, no slow pip resolves.
This blog itself uses `uv` to manage its dependencies.

I've switched to it for every Python project I touch.
