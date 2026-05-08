"""
MkDocs hook that:
1. Auto-generates per-category post lists in docs/likes/index.md
2. Injects latest-posts and latest-likes sections into docs/index.md

For likes/index.md, wrap each section in a block comment:

    <!-- likes:Tools
    ## Tools I like
    Your description here.
    -->

For index.md, use single-line placeholders:

    <!-- overview:latest-posts -->
    <!-- overview:latest-likes -->

Draft handling: post lists are sourced from the blog plugin's resolved post
list, so any post excluded by the blog plugin (drafts, future-dated, etc.) is
automatically omitted here too.
"""

import re
from datetime import timedelta
from re import Match
from typing import Any

PLACEHOLDER = re.compile(r"<!-- likes:(.+?)\n(.*?)-->", re.DOTALL)
OVERVIEW_PLACEHOLDER = re.compile(r"<!-- overview:(.+?) -->")

_blog_posts: list[dict[str, Any]] = []
_likes_posts: list[dict[str, Any]] = []


def on_files(_files: Any, *, config: Any, **__: Any) -> None:
    _blog_posts.clear()
    _likes_posts.clear()
    for _name, plugin in config["plugins"].items():
        posts = getattr(getattr(plugin, "blog", None), "posts", None)
        if posts is None:
            continue
        blog_dir = getattr(getattr(plugin, "config", None), "blog_dir", None)
        is_likes = (blog_dir == "likes/feed")
        for post in posts:
            categories = post.meta.get("categories") or []
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
            }
            if is_likes:
                if not categories:
                    continue
                for cat in categories:
                    _likes_posts.append({**entry, "category": cat})
            else:
                _blog_posts.append(entry)

on_files.mkdocs_priority = -75  # type: ignore[attr-defined]  # run after blog plugin (priority -50)


def _latest_window(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not posts:
        return []
    sorted_posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    cutoff = sorted_posts[0]["date"] - timedelta(days=7)
    return [p for p in sorted_posts if p["date"] >= cutoff]


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


def _build_list(category: str, section: str) -> str:
    matching = [p for p in _likes_posts if p["category"] == category]
    matching.sort(key=lambda p: p["date"], reverse=True)
    if not matching:
        return ""
    rows = []
    for p in matching:
        date_str = p["date"].strftime("%Y-%m-%d")
        rows.append(
            f'<a class="likes-row" href="{p["slug"]}/">'
            f'<span class="likes-title">{p["title"]}</span>'
            f'<span class="likes-date">{date_str}</span>'
            f'</a>'
        )
    list_html = '<div class="likes-list">\n' + "\n".join(rows) + "\n</div>"
    return section + "\n" + list_html


def on_page_markdown(markdown: str, page: Any, **__: Any) -> str:
    if page.file.src_path == "likes/index.md":
        def replace_likes(m: Match[str]) -> str:
            return _build_list(m.group(1).strip(), m.group(2).strip())
        return PLACEHOLDER.sub(replace_likes, markdown)

    if page.file.src_path == "index.md":
        def replace_overview(m: Match[str]) -> str:
            key = m.group(1).strip()
            if key == "latest-posts":
                return _render_rows(_latest_window(_blog_posts))
            if key == "latest-likes":
                seen: set[str] = set()
                unique: list[dict[str, Any]] = []
                for p in _latest_window(_likes_posts):
                    if p["slug"] not in seen:
                        seen.add(p["slug"])
                        unique.append(p)
                return _render_rows(unique)
            return m.group(0)
        return OVERVIEW_PLACEHOLDER.sub(replace_overview, markdown)

    return markdown
