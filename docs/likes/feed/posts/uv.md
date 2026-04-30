---
date: 2026-04-24
categories:
  - Tools
---

# uv

[uv](https://docs.astral.sh/uv/) is a Python package and project manager written in Rust, built by [Astral](https://astral.sh).

<!-- more -->

It replaces `pip`, `pip-tools`, `pipx`, `virtualenv`, `pyenv`, and parts of `poetry` — all in one tool, and drastically faster.

What I like most about it: it just works.
Drop in a `pyproject.toml`, run `uv sync`, and you have a reproducible environment in seconds.
No fussing with virtualenvs, no slow pip resolves.
This blog itself uses `uv` to manage its dependencies.

I've switched to it for every Python project I touch.
