"""
MkDocs hook that:
1. Generates tag styles CSS from mkdocs.yml extra.tags config
2. Auto-generates per-tag post lists in docs/likes/index.md
3. Injects latest-posts and latest-likes sections into docs/index.md

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

Tag colors: defined in mkdocs.yml under extra.tags, generated as CSS at build time.
"""

import re
from pathlib import Path
from re import Match
from typing import Any

PLACEHOLDER = re.compile(r"<!-- likes:(.+?)\n(.*?)-->", re.DOTALL)
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
        is_likes = (blog_dir == "likes/feed")
        for post in posts:
            tags = post.meta.get("tags") or []
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
                if tags:
                    for tag in tags:
                        _likes_posts.append({**entry, "tag": tag})
                else:
                    _likes_posts.append({**entry, "tag": "Others"})
            else:
                _blog_posts.append(entry)

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


def _build_list(tag: str, section: str) -> str:
    matching = [p for p in _likes_posts if p["tag"] == tag]
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
        valid_tags = set(m.group(1).strip() for m in PLACEHOLDER.finditer(markdown))

        def replace_likes(m: Match[str]) -> str:
            tag = m.group(1).strip()
            section = m.group(2).strip()
            if tag == "Others":
                # Others = posts that don't have ANY tag in valid_tags (by slug)
                posts_with_valid_tags = set()
                for p in _likes_posts:
                    if p["tag"] in valid_tags:
                        posts_with_valid_tags.add(p["slug"])
                # Deduplicate by slug (a post may have multiple invalid tags)
                seen = set()
                matching = []
                for p in _likes_posts:
                    if p["slug"] not in posts_with_valid_tags and p["slug"] not in seen:
                        matching.append(p)
                        seen.add(p["slug"])
            else:
                matching = [p for p in _likes_posts if p["tag"] == tag]
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
        return PLACEHOLDER.sub(replace_likes, markdown)

    if page.file.src_path == "index.md":
        def replace_overview(m: Match[str]) -> str:
            key = m.group(1).strip()
            if key == "latest-posts":
                return _render_rows(_latest_groups(_blog_posts))
            if key == "latest-likes":
                seen: set[str] = set()
                unique: list[dict[str, Any]] = []
                for p in _likes_posts:
                    if p["slug"] not in seen:
                        seen.add(p["slug"])
                        unique.append(p)
                return _render_rows(_latest_groups(unique))
            return m.group(0)
        return OVERVIEW_PLACEHOLDER.sub(replace_overview, markdown)

    return markdown
