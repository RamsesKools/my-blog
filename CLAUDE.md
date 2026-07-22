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

`mkdocs.yml` configures the `blog` plugin twice — once for actual posts (`docs/posts/` → `blog/`) and once for the "Things I Like" posts (`docs/likes/posts/` → `likes/`). Both disable `pagination` and `categories` (unused) and use flat post URLs (no date prefix): the blog instance via `post_url_format: "../{slug}"`, the likes instance via `post_url_format: "{slug}"` since its `blog_dir` is already `likes`.

Both `docs/blog/index.md` and `docs/likes/index.md` set `template: main.html` in frontmatter, which overrides the blog plugin's default `template: blog.html` (a `meta.setdefault` the plugin only applies if the page doesn't already set one) — this makes them render as plain content pages instead of getting an auto-generated post list/pagination appended. The actual post listing on both pages is hand-rendered by `blog_hooks.py` instead (see below).

### `blog_hooks.py` — custom MkDocs hook

This is the one piece of non-obvious machinery. It is registered both as a `hook` and under `watch` in `mkdocs.yml`. Its `on_files` runs after the blog plugin (`mkdocs_priority = -75`, blog plugin is `-50`) so it can read the resolved post lists — meaning drafts and future-dated posts the blog plugin already filtered out are automatically excluded here too.

It does three things:

1. On `docs/blog/index.md` and `docs/likes/index.md`, replaces a single-line `<!-- tag-index:blog -->` / `<!-- tag-index:likes -->` placeholder with an alphabetical tag "cloud" of clickable pills followed by a table of all posts (title, created date, tags). Clicking a tag pill filters the table client-side (see `docs/assets/tag-filter.js`) — OR logic across multiple selected tags, deselecting all tags shows everything again. Posts with `draft: true` (only ever visible locally, since `draft_on_serve: true`) get a small "Draft" badge next to the title.
2. In `docs/index.md`, replaces `<!-- overview:latest-posts -->` and `<!-- overview:latest-likes -->` with rows for the latest items: whole same-date groups are added newest first, and no further group is added once the list has at least 3 items (so ties can make the list longer than 3).
3. Writes `site/assets/post-preview.json`, keyed by URL, consumed by `docs/assets/link-preview.js` to show a hover-card preview over internal links. Each entry's `excerptHtml` is the Markdown up to that page's `<!-- more -->` marker, rendered through a standalone `markdown.Markdown()` instance built from the same `markdown_extensions`/`mdx_configs` as the real build — so headings, code blocks, links, and images keep their formatting in the card. See [Post excerpts and the hover preview](#post-excerpts-and-the-hover-preview) below. Note: this standalone converter doesn't run the `ezlinks` plugin, so `[[wikilinks]]` inside an excerpt degrade to plain text rather than a resolved link.

The tag-index table uses `.tag-filter` / `.tag-cloud` / `.tag-filter-table` / `.tag-filter-row` classes; the homepage overview rows still use the older `.likes-list` / `.likes-row` / `.likes-title` / `.likes-date` classes. Both are styled in `docs/assets/custom.css`.

### Theme overrides

`overrides/` is the Material theme `custom_dir`. `overrides/partials/header.html` and `nav.html` override stock partials; `overrides/blog-post.html` overrides the blog post template.

## Content conventions

### Embedding videos

Store videos in `docs/assets/` and embed with a plain `<video>` tag using an **absolute** `src="/assets/..."`. Relative paths break because `use_directory_urls: true` restructures page URLs. To convert a screen recording before committing:

```bash
ffmpeg -i input.mov -vcodec h264 -acodec aac -crf 28 -preset slow docs/assets/output.mp4
```

### Compressing images

Store images in `docs/assets/` as JPEG with 85% quality to balance file size and visual fidelity. Convert PNG images before committing using `sips` (built into macOS):

```bash
sips -s format jpeg -s formatOptions 85 input.png --out docs/assets/output.jpg
```

This typically reduces file size by 70-80%. Use absolute paths in Markdown (`![alt](/assets/filename.jpg)`) so images load correctly regardless of page depth.

### Post excerpts and the hover preview

Every post and page that should get a hover-card preview needs a `<!-- more -->` marker after its intro paragraph(s) — the marker is what `blog_hooks.py` cuts the excerpt at (see [`blog_hooks.py`](#blog_hookspy--custom-mkdocs-hook) above). Everything before it is rendered through the real Markdown pipeline and shown verbatim in the hover card, so:

- Write the intro so it reads well standalone — it's the actual preview text, not just a plain-text summary anymore.
- Headings, code blocks, links, and images in that section keep their formatting in the card.
- `[[wikilinks]]` inside the excerpt degrade to plain unlinked text (the `ezlinks` plugin that resolves them doesn't run in the standalone converter used for previews).
- If a page has no `<!-- more -->` marker, the *entire* page becomes the excerpt and a build warning is logged — always add the marker rather than rely on that fallback.

Always check the rendered hover preview locally before publishing: run `uv run mkdocs serve`, hover an internal link to the new post/page, and confirm the card looks right (not overflowing, nothing look broken).

### Adding a "like"

Create a Markdown file under `docs/likes/posts/` with frontmatter that includes `date:` and `tags:` (e.g. `Tools`, `People`, `Products`, `Websites`, `Movies`). Tags drive the tag-cloud filter on `docs/likes/index.md` — no separate registration step needed, any tag used on a post automatically appears in the cloud.

### Post metadata: tags, dates, and custom fields

All posts (blog and likes) support **tags** and optional **created/updated date distinction**. Custom metadata fields can be added to individual posts and will automatically render in the post's sidebar "Metadata" block.

#### Tags

Add `tags:` as a list to any post frontmatter:

```yaml
---
date: 2026-05-12
tags:
  - Tools
  - DevOps
  - Infrastructure
---
```

Tags render as pill-shaped chips above the post title. They're also clickable, filterable elements on the tag-cloud overview pages — see `docs/blog/index.md` and `docs/likes/index.md`.

##### Customizing tag colors

Tag colors are defined in `mkdocs.yml` under `extra.tags`. Each tag entry specifies `bg` (background), `text` (text color), and optionally `border`:

```yaml
extra:
  tags:
    Tools:
      bg: "#D6E4FA"
      text: "#1E4A9C"
    AI:
      bg: "#E8F0FF"
      text: "#1A3A8A"
      border: "1px solid #1A3A8A"
```

Tag colors are generated at build time (via the `on_config` and `on_post_build` hooks in `blog_hooks.py`) and appended to the final `site/assets/custom.css` file. No source file changes needed — just edit the YAML config and rebuild.

#### Created and updated dates

Use `date:` as a dict to distinguish **created** and **updated** dates:

```yaml
---
date:
  created: 2026-05-12
  updated: 2026-07-01
---
```

Both dates appear in the "Metadata" sidebar; only `created` is used for chronological sorting. Existing scalar `date: 2026-05-12` posts are internally normalized to `{created: 2026-05-12}` and continue to work unchanged.

#### Custom metadata fields

Any frontmatter field not in the reserved list (date, categories, tags, slug, draft, authors, links, readtime, hide, title, description, template, icon) is automatically rendered as a row in the post's "Metadata" sidebar with a generic icon and `Key: value` format.

Two special cases are built in:

1. **`rating`** — a 0-10 integer rendered as a 5-star scale. Example:

```yaml
rating: 9
```

Displays as `★★★★½ 9/10` (4 full stars + 1 half star for `9/10`).

2. Other custom fields render as plain text. Example:

```yaml
myfield: "Some value"
```

Displays as `Myfield: Some value` with an info icon.

To add a new special-cased field with custom rendering (e.g. a badge, colored pill, or different icon), edit `overrides/blog-post.html` lines 102–110 to add a `{% if page.meta.myfield %}` block following the same pattern as the `rating` block.

### Markdown extensions enabled

`attr_list`, `pymdownx.blocks.caption`, and `pymdownx.superfences` with a `mermaid` fence — so ` ```mermaid ` code blocks render as diagrams.

## Writing style

The user prefers concise, light, extroverted prose. Avoid em-dashes, unicode flourishes, and emojis unless specifically asked. One sentence per line in Markdown. Prefer linking to and briefly quoting existing writing over re-explaining it. Avoid horizontal rules (`---`) unless necessary.
