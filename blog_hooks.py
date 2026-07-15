"""
MkDocs hook that:
1. Generates tag styles CSS from mkdocs.yml extra.tags config
2. Renders a clickable tag-cloud + post table on docs/blog/index.md and
   docs/likes/index.md via a single-line placeholder
3. Injects latest-posts and latest-likes sections into docs/index.md
4. Writes a post-preview JSON file (title/synopsis/tags/readtime per post,
   keyed by URL) for the hover-card link preview in docs/assets/link-preview.js

For docs/blog/index.md and docs/likes/index.md, use a single-line placeholder:

    <!-- tag-index:blog -->
    <!-- tag-index:likes -->

For index.md, use single-line placeholders:

    <!-- overview:latest-posts -->
    <!-- overview:latest-likes -->

Draft handling: post lists are sourced from the blog plugin's resolved post
list, so any post excluded by the blog plugin (drafts, future-dated, etc.) is
automatically omitted here too. When draft_on_serve makes drafts visible
(local `mkdocs serve`), they carry a small "Draft" marker in the rendered table.

Tag colors: defined in mkdocs.yml under extra.tags, generated as CSS at build time.

Synopsis/readtime: computed from each post's raw Markdown source (not the
rendered HTML) so the data is available immediately in on_files, independent
of per-page build order.
"""

import json
import posixpath
import re
from math import ceil
from pathlib import Path
from re import Match
from typing import Any

TAG_INDEX_PLACEHOLDER = re.compile(r"<!-- tag-index:(blog|likes) -->")
OVERVIEW_PLACEHOLDER = re.compile(r"<!-- overview:(.+?) -->")

WORDS_PER_MINUTE = 265
SYNOPSIS_LENGTH = 200

_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_WIKILINK_PIPED_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")
_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MD_SYMBOLS_RE = re.compile(r"[#*_>`~|]")
_WHITESPACE_RE = re.compile(r"\s+")

_blog_posts: list[dict[str, Any]] = []
_likes_posts: list[dict[str, Any]] = []
_post_preview_json = "{}"


def _plain_text(markdown_text: str) -> str:
    """Strip frontmatter, Markdown syntax, and raw HTML down to plain text."""
    text = _FRONTMATTER_RE.sub("", markdown_text, count=1)
    text = _CODE_FENCE_RE.sub(" ", text)
    text = _IMAGE_RE.sub(" ", text)
    text = _WIKILINK_PIPED_RE.sub(r"\2", text)
    text = _WIKILINK_RE.sub(r"\1", text)
    text = _LINK_RE.sub(r"\1", text)
    text = _HTML_TAG_RE.sub(" ", text)
    text = _MD_SYMBOLS_RE.sub(" ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def _synopsis_and_readtime(markdown_text: str) -> tuple[str, int]:
    text = _plain_text(markdown_text)
    words = text.split(" ") if text else []
    readtime = max(1, ceil(len(words) / WORDS_PER_MINUTE))

    synopsis = text
    if len(synopsis) > SYNOPSIS_LENGTH:
        cutoff = synopsis.rfind(" ", 0, SYNOPSIS_LENGTH)
        if cutoff == -1:
            cutoff = SYNOPSIS_LENGTH
        synopsis = synopsis[:cutoff].rstrip() + "…"
    return synopsis, readtime


def on_config(config: Any, **__: Any) -> None:
    """Generate tag styles CSS from mkdocs.yml extra.tags config and store in memory."""
    tags = config.get("extra", {}).get("tags", {})
    if not tags:
        return

    css_lines = ["/* Generated tag styles from mkdocs.yml extra.tags */\n"]
    for tag_name, tag_spec in tags.items():
        bg = tag_spec.get("bg", "#E0E0E0")
        text = tag_spec.get("text", "#424242")
        border = tag_spec.get("border", "")

        css = f'.md-tag-pill[data-tag="{tag_name}"] {{\n'
        css += f'    background: {bg};\n'
        css += f'    color: {text};\n'
        if border:
            css += f'    border: {border};\n'
        css += "}\n"
        css_lines.append(css)

    # Store generated CSS in config.extra for use in on_post_build
    config.setdefault("extra", {})["tags_css"] = "\n".join(css_lines)

on_config.mkdocs_priority = 100  # type: ignore[attr-defined]  # run early, before other plugins


def on_files(_files: Any, *, config: Any, **__: Any) -> None:
    global _post_preview_json
    _blog_posts.clear()
    _likes_posts.clear()
    for _name, plugin in config["plugins"].items():
        posts = getattr(getattr(plugin, "blog", None), "posts", None)
        if posts is None:
            continue
        blog_dir = getattr(getattr(plugin, "config", None), "blog_dir", None)
        is_likes = (blog_dir == "likes")
        for post in posts:
            date = getattr(getattr(post, "config", None), "date", None)
            created = getattr(date, "created", None)
            # post_url_format can contain "../" (e.g. the main blog's
            # "../{slug}"); normalize it so it matches the browser's
            # normalized link.pathname used by link-preview.js.
            url = posixpath.normpath(post.url) + "/"
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            if not (post.title and created):
                continue
            markdown_text = Path(post.file.abs_src_path).read_text(encoding="utf-8")
            synopsis, readtime = _synopsis_and_readtime(markdown_text)
            entry = {
                "title": post.title,
                "date": created,
                "slug": slug,
                "url": url,
                "tags": list(post.meta.get("tags") or []),
                "draft": bool(post.meta.get("draft", False)),
                "synopsis": synopsis,
                "readtime": readtime,
            }
            (_likes_posts if is_likes else _blog_posts).append(entry)

    preview = {
        f'/{p["url"]}': {
            "title": p["title"],
            "date": p["date"].strftime("%Y-%m-%d"),
            "tags": p["tags"],
            "draft": p["draft"],
            "synopsis": p["synopsis"],
            "readtime": p["readtime"],
        }
        for p in (*_blog_posts, *_likes_posts)
    }
    _post_preview_json = json.dumps(preview)

on_files.mkdocs_priority = -75  # type: ignore[attr-defined]  # run after blog plugin (priority -50)


def on_post_build(config: Any, **__: Any) -> None:
    """Append generated tag CSS to custom.css and write the post-preview JSON."""
    site_dir = Path(config.get("site_dir", "site"))

    tags_css = config.get("extra", {}).get("tags_css")
    custom_css = site_dir / "assets" / "custom.css"
    if tags_css and custom_css.exists():
        current_css = custom_css.read_text()
        custom_css.write_text(current_css + "\n" + tags_css)

    preview_path = site_dir / "assets" / "post-preview.json"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(_post_preview_json)

on_post_build.mkdocs_priority = -100  # type: ignore[attr-defined]  # run after all other processing


def _latest_groups(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Newest first, whole same-date groups, stop adding groups once we have 3+."""
    sorted_posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    selected: list[dict[str, Any]] = []
    for post in sorted_posts:
        if len(selected) >= 3 and post["date"].date() != selected[-1]["date"].date():
            break
        selected.append(post)
    return selected


def _render_rows(posts: list[dict[str, Any]]) -> str:
    if not posts:
        return ""
    rows: list[str] = []
    for p in posts:
        date_str = p["date"].strftime("%Y-%m-%d")
        rows.append(
            f'<a class="likes-row" href="/{p["url"]}">'
            f'<span class="likes-title">{p["title"]}</span>'
            f'<span class="likes-date">{date_str}</span>'
            f'</a>'
        )
    return '<div class="likes-list">\n' + "\n".join(rows) + "\n</div>"


def _render_tag_index(posts: list[dict[str, Any]]) -> str:
    """Render a clickable tag cloud plus a filterable table of all posts."""
    if not posts:
        return "<p><em>Nothing here yet.</em></p>"

    all_tags = sorted({tag for p in posts for tag in p["tags"]})
    cloud = ""
    if all_tags:
        buttons = "\n".join(
            f'<button type="button" class="md-tag-pill md-tag-pill--filter" '
            f'data-tag="{tag}" aria-pressed="false">{tag}</button>'
            for tag in all_tags
        )
        clear_button = (
            '<button type="button" class="md-tag-pill--clear" '
            'data-tag-clear disabled aria-label="Clear selected tags">&times;</button>'
        )
        cloud = f'<div class="tag-cloud" data-tag-filter-cloud>\n{buttons}\n{clear_button}\n</div>'

    rows: list[str] = []
    for p in sorted(posts, key=lambda p: p["date"], reverse=True):
        date_str = p["date"].strftime("%Y-%m-%d")
        tags_attr = ",".join(p["tags"])
        pills = "".join(
            f'<span class="md-tag-pill" data-tag="{t}">{t}</span>' for t in p["tags"]
        )
        draft_marker = (
            ' <span class="tag-filter-draft-marker" title="Draft">Draft</span>'
            if p["draft"] else ""
        )
        rows.append(
            f'<div class="tag-filter-row" data-tags="{tags_attr}">'
            f'<span class="tag-filter-title"><a href="/{p["url"]}">{p["title"]}</a>{draft_marker}</span>'
            f'<span class="tag-filter-meta">'
            f'<span class="tag-filter-tags">{pills}</span>'
            f'<span class="tag-filter-date">{date_str}</span>'
            f'</span>'
            f'</div>'
        )

    list_html = '<div class="tag-filter-list" data-tag-filter-list>\n' + "\n".join(rows) + "\n</div>"
    empty_html = (
        '<p class="tag-filter-empty" data-tag-filter-empty style="display:none">'
        'No posts match the selected tags.</p>'
    )

    return f'<div class="tag-filter" data-tag-filter>\n{cloud}\n{list_html}\n{empty_html}\n</div>'


def on_page_markdown(markdown: str, page: Any, **__: Any) -> str:
    if page.file.src_path in ("blog/index.md", "likes/index.md"):
        def replace_tag_index(m: Match[str]) -> str:
            key = m.group(1)
            return _render_tag_index(_blog_posts if key == "blog" else _likes_posts)
        return TAG_INDEX_PLACEHOLDER.sub(replace_tag_index, markdown)

    if page.file.src_path == "index.md":
        def replace_overview(m: Match[str]) -> str:
            key = m.group(1).strip()
            if key == "latest-posts":
                return _render_rows(_latest_groups(_blog_posts))
            if key == "latest-likes":
                return _render_rows(_latest_groups(_likes_posts))
            return m.group(0)
        return OVERVIEW_PLACEHOLDER.sub(replace_overview, markdown)

    return markdown
