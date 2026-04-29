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
import yaml


PLACEHOLDER = re.compile(r"<!-- likes:(.+?) -->")


def _read_posts(docs_dir: str) -> list[dict]:
    posts_dir = Path(docs_dir) / "likes" / "posts"
    posts = []
    for md_file in posts_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.index("---", 3)
        front = yaml.safe_load(text[3:end])
        body = text[end + 3:].lstrip("\n")
        title = None
        for line in body.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if title and front.get("categories") and front.get("date"):
            for cat in front["categories"]:
                posts.append({
                    "title": title,
                    "date": front["date"],
                    "category": cat,
                    "slug": md_file.stem,
                })
    return posts


def _build_list(posts: list[dict], category: str) -> str:
    matching = [p for p in posts if p["category"] == category]
    matching.sort(key=lambda p: p["date"], reverse=True)
    if not matching:
        return "*Nothing here yet.*"
    lines = [f"- [{p['title']}](posts/{p['slug']}.md)" for p in matching]
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files, **kwargs):
    if page.file.src_path != "likes/index.md":
        return markdown
    posts = _read_posts(config["docs_dir"])

    def replace(m):
        return _build_list(posts, m.group(1).strip())

    return PLACEHOLDER.sub(replace, markdown)
