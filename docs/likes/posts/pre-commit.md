---
date: 2026-07-15
categories:
  - Tools
draft: true
tags:
  - Tools
  - DevOps
---

# <img src="/assets/pre-commit.png" alt="pre-commit logo" style="height:1em; vertical-align:middle; display:inline;"> pre-commit

[pre-commit](https://pre-commit.com) is a framework for managing and running git hooks.

<!-- more -->

Define a `.pre-commit-config.yaml` in your repo and it will automatically run linters, formatters, and checks before every commit — across any language.

The value is in the consistency: the same checks run locally for every developer and in CI, with no manual setup beyond installing the hooks once (`pre-commit install`).
It catches small issues (trailing whitespace, secrets accidentally staged, broken JSON) before they ever hit a review or pipeline.
