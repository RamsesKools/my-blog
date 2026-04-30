"""
MkDocs hook that auto-generates per-category post lists in docs/likes/index.md.

In index.md, write a section like:

    ## Tools I like
    Your description here.
    <!-- likes:Tools -->

The hook replaces each <!-- likes:<Category> --> comment with a bullet list of
posts in that category, sorted by date descending.
"""

import re
from pathlib import Path
from re import Match
from typing import Any
import yaml
from pymdownx.slugs import slugify as _slugify  # type: ignore[import-untyped]

_slugify_post = _slugify(case="lower")


PLACEHOLDER = re.compile(r"<!-- likes:(.+?) -->")


def _read_posts(docs_dir: str) -> list[dict[str, Any]]:
    posts_dir = Path(docs_dir) / "likes" / "feed" / "posts"
    posts: list[dict[str, Any]] = []
    for md_file in posts_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.index("---", 3)
        front: dict[str, Any] = yaml.safe_load(text[3:end])
        body = text[end + 3:].lstrip("\n")
        title: str | None = None
        for line in body.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if title and front.get("categories") and front.get("date"):
            slug = front.get("slug") or _slugify_post(title, "-")
            for cat in front["categories"]:
                posts.append({
                    "title": title,
                    "date": front["date"],
                    "category": cat,
                    "slug": slug,
                })
    return posts


def _build_list(posts: list[dict[str, Any]], category: str) -> str:
    matching = [p for p in posts if p["category"] == category]
    matching.sort(key=lambda p: p["date"], reverse=True)
    if not matching:
        return "*Nothing here yet.*"
    rows = []
    for p in matching:
        date_str = p["date"].strftime("%Y-%m-%d") if hasattr(p["date"], "strftime") else str(p["date"])
        rows.append(
            f'<a class="likes-row" href="{p["slug"]}/">'
            f'<span class="likes-title">{p["title"]}</span>'
            f'<span class="likes-date">{date_str}</span>'
            f'</a>'
        )
    return '<div class="likes-list">\n' + "\n".join(rows) + "\n</div>"


def on_page_markdown(markdown: str, page: Any, config: Any, **__: Any) -> str:
    if page.file.src_path != "likes/index.md":
        return markdown
    posts = _read_posts(config["docs_dir"])

    def replace(m: Match[str]) -> str:
        return _build_list(posts, m.group(1).strip())

    return PLACEHOLDER.sub(replace, markdown)
