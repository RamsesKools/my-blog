"""
MkDocs hook that auto-generates per-category post lists in docs/likes/index.md.

In index.md, wrap each section in a block comment like:

    <!-- likes:Tools
    ## Tools I like
    Your description here.
    -->

The hook renders the heading, description, and post list when the category has
posts, and removes the entire block when it is empty.

Draft handling: the post list is sourced from the blog plugin's resolved post
list, so any post excluded by the blog plugin (drafts, future-dated, etc.) is
automatically omitted here too.
"""

import re
from re import Match
from typing import Any

PLACEHOLDER = re.compile(r"<!-- likes:(.+?)\n(.*?)-->", re.DOTALL)

_posts: list[dict[str, Any]] = []


def on_files(_files: Any, *, config: Any, **__: Any) -> None:
    _posts.clear()
    for _name, plugin in config["plugins"].items():
        posts = getattr(getattr(plugin, "blog", None), "posts", None)
        if posts is None:
            continue
        for post in posts:
            categories = post.meta.get("categories") or []
            date = getattr(getattr(post, "config", None), "date", None)
            created = getattr(date, "created", None)
            slug = post.url.rstrip("/").rsplit("/", 1)[-1]
            if post.title and categories and created:
                for cat in categories:
                    _posts.append({
                        "title": post.title,
                        "date": created,
                        "category": cat,
                        "slug": slug,
                    })

on_files.mkdocs_priority = -75  # type: ignore[attr-defined]  # run after blog plugin (priority -50)


def _build_list(category: str, section: str) -> str:
    matching = [p for p in _posts if p["category"] == category]
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
    if page.file.src_path != "likes/index.md":
        return markdown

    def replace(m: Match[str]) -> str:
        return _build_list(m.group(1).strip(), m.group(2).strip())

    return PLACEHOLDER.sub(replace, markdown)
