"""
MkDocs hook that:
1. Generates tag styles CSS from mkdocs.yml extra.tags config
2. Renders a clickable tag-cloud + post table on docs/blog/index.md and
   docs/likes/index.md via a single-line placeholder
3. Injects latest-posts and latest-likes sections into docs/index.md

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
"""

import re
from pathlib import Path
from re import Match
from typing import Any

TAG_INDEX_PLACEHOLDER = re.compile(r"<!-- tag-index:(blog|likes) -->")
OVERVIEW_PLACEHOLDER = re.compile(r"<!-- overview:(.+?) -->")

_blog_posts: list[dict[str, Any]] = []
_likes_posts: list[dict[str, Any]] = []


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
            slug = post.url.rstrip("/").rsplit("/", 1)[-1]
            if not (post.title and created):
                continue
            entry = {
                "title": post.title,
                "date": created,
                "slug": slug,
                "url": post.url,
                "tags": list(post.meta.get("tags") or []),
                "draft": bool(post.meta.get("draft", False)),
            }
            (_likes_posts if is_likes else _blog_posts).append(entry)

on_files.mkdocs_priority = -75  # type: ignore[attr-defined]  # run after blog plugin (priority -50)


def on_post_build(config: Any, **__: Any) -> None:
    """Append generated tag CSS to the built custom.css file."""
    tags_css = config.get("extra", {}).get("tags_css")
    if not tags_css:
        return

    site_dir = Path(config.get("site_dir", "site"))
    custom_css = site_dir / "assets" / "custom.css"

    if custom_css.exists():
        current_css = custom_css.read_text()
        custom_css.write_text(current_css + "\n" + tags_css)

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
        cloud = f'<div class="tag-cloud" data-tag-filter-cloud>\n{buttons}\n</div>'

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
