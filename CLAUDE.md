# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Personal blog built with MkDocs Material. Content is Markdown under `docs/`, the site is built to `site/`, and there are two deployment targets:

- `blog.ramseskools.nl` — public, GitHub Pages, deployed via `.github/workflows/deploy-gh-pages.yml` on release publish or manual `workflow_dispatch` (which auto-creates a CalVer tag `YYYY.MM.DD`).
- `blog-preview.ramseskools.nl` — private preview, served by the nginx container in `docker-compose.yml`. A Dagu DAG (`blog-preview-deploy`) on the host polls this repo every 5 minutes and rebuilds with `mkdocs build`.

## Common commands

Dependencies are managed with `uv` (see `pyproject.toml` / `uv.lock`). Run mkdocs through `uv run`:

- `uv run mkdocs serve` — local dev server with live reload (drafts are visible because `draft_on_serve: true` is set on both blog plugins).
- `uv run mkdocs build` — produce `site/`. This is what both deployment targets run.

There are no tests, linters, or formatters configured in this repo.

## Architecture

### Two blog plugins, one site

`mkdocs.yml` configures the `blog` plugin twice — once for actual posts (`docs/posts/` → `blog/`) and once for the "Things I Like" feed (`docs/likes/feed/posts/` → `likes/feed/`). Both use `post_url_format: "../{slug}"` so post URLs are flat (no date prefix).

### `likes_index_plugin.py` — custom MkDocs hook

This is the one piece of non-obvious machinery. It is registered both as a `hook` and under `watch` in `mkdocs.yml`. It runs after the blog plugin (`mkdocs_priority = -75`, blog plugin is `-50`) so it can read the resolved post lists — meaning drafts and future-dated posts the blog plugin already filtered out are automatically excluded here too.

It does two things:

1. In `docs/likes/index.md`, expands `<!-- likes:CategoryName ... -->` block comments into a section header plus an HTML list of all "likes" posts whose frontmatter `categories:` includes that category. Posts without categories are skipped.
2. In `docs/index.md`, replaces `<!-- overview:latest-posts -->` and `<!-- overview:latest-likes -->` with rows for the latest items: whole same-date groups are added newest first, and no further group is added once the list has at least 3 items (so ties can make the list longer than 3).

Rendered rows use the `.likes-list` / `.likes-row` / `.likes-title` / `.likes-date` classes styled in `docs/assets/custom.css`.

### Theme overrides

`overrides/` is the Material theme `custom_dir`. `overrides/partials/header.html` and `nav.html` override stock partials; `overrides/blog-post.html` overrides the blog post template.

## Content conventions

### Embedding videos

Store videos in `docs/assets/` and embed with a plain `<video>` tag using an **absolute** `src="/assets/..."`. Relative paths break because `use_directory_urls: true` restructures page URLs. To convert a screen recording before committing:

```bash
ffmpeg -i input.mov -vcodec h264 -acodec aac -crf 28 -preset slow docs/assets/output.mp4
```

### Adding a "like"

Create a Markdown file under `docs/likes/feed/posts/` with frontmatter that includes `date:` and `categories:` (e.g. `Tools`, `People`, `Products`, `Websites`, `Movies`). The category drives which section it lands in on `docs/likes/index.md`. To add a brand-new category, add a matching `<!-- likes:NewCategory ... -->` block to `docs/likes/index.md`.

### Markdown extensions enabled

`attr_list`, `pymdownx.blocks.caption`, and `pymdownx.superfences` with a `mermaid` fence — so ` ```mermaid ` code blocks render as diagrams.

## Writing style

The user prefers concise, light, extroverted prose. Avoid em-dashes, unicode flourishes, and emojis unless specifically asked. One sentence per line in Markdown. Prefer linking to and briefly quoting existing writing over re-explaining it. Avoid horizontal rules (`---`) unless necessary.
