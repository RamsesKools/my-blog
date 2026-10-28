---
name: linkedin-blog-post
description: Draft a LinkedIn post announcing one or more posts from this blog. Use when the user asks for a LinkedIn post, LinkedIn update, or "share this on LinkedIn" about a blog post or posts. Produces a short English + Dutch text block in the user's voice, always with the full post URLs, and points at a hero image to attach if the post has one.
---

# linkedin-blog-post

Write a short LinkedIn announcement for one or more posts on this blog and hand it back as a text block the user pastes into LinkedIn.
You are only writing copy. Do not post anywhere.

## Output shape

One fenced text block, English first, then Dutch directly under it (blank line between).
Keep it to a few lines. One line of description per post, first person, about what it does for the user.

```
Hey all, I have another small blog update.
Dutch follows English.
I would like to share <two tools I recently added to my AI Coding stack / a tool / etc.> with you:
- <Title>: <full blog URL>
- <Title>: <full blog URL>

<Title> <one line on what it does for me>.

<Title> <one line on what it does for me>.

Hoi allemaal, weer een kleine blog update.
Ik wil <twee nieuwe tools delen die ik recent aan mijn AI Coding stack heb toegevoegd / een tool>:
- <Title>: <full blog URL>
- <Title>: <full blog URL>

Met <Title> <een regel, informeel>.

Met <Title> <een regel, informeel>.
```

Keep `Dutch follows English.` as a fixed signpost line right under the greeting.

Output the full canonical blog URLs (`https://blog.ramseskools.nl/...`).
LinkedIn rewrites them to `lnkd.in` short links on its own once the post is live, so do not try to produce those.

After the block, on a normal line (not in the block), name the image file(s) to attach, e.g.
`Attach: docs/assets/gitops-ai-agents-architecture.png`.
If no post has a strong image, say so in one line.

## Style

Follows the user's global writing style plus:

- Light, friendly, extroverted. "Hey all," / "Hoi allemaal,".
- Concise. A few lines total, not a paragraph per post.
- First person and concrete: "lets me...", "Met X zie ik...".
- The intro line says where the tools fit, e.g. "two tools I recently added to my AI Coding stack". Scale to the count.
- No em-dashes, no emojis, no unicode flourishes.
- Plain URLs, not markdown links. LinkedIn auto-links them.
- Dutch is a casual, informal rewrite, not a word-for-word translation. Loose spoken register: "vet" for cool, "vast lopen" for erroring, "mijn input willen" for needing me. Not formal Dutch.

## Steps

### 1. Identify the posts

The user names them ("codeburn and peon-ping", "my latest like", "these two").
Blog posts live in `docs/posts/`, likes in `docs/likes/posts/`.

### 2. Resolve the canonical URLs

The reliable source is the built site.

```bash
uv run mkdocs build
python3 -c "import json,sys; d=json.load(open('site/assets/post-preview.json')); [print('https://blog.ramseskools.nl'+k) for k in sorted(d)]"
```

`post-preview.json` is keyed by path. Prefix each key with `https://blog.ramseskools.nl`.

- Likes render at `https://blog.ramseskools.nl/likes/<slug>/`.
- Blog posts render at `https://blog.ramseskools.nl/<slug>/` (root level, no `/blog/` segment).
- `<slug>` is the frontmatter `slug:` when present, otherwise a slugified title, so do not guess it. Read it from `post-preview.json`.

If a URL is ambiguous, match on the post title from the source file's H1.

### 3. Write the one-liner per post

Read the intro of each source file, the part before the `<!-- more -->` marker.
Turn it into one plain sentence in the user's voice about what the tool or post does for them.
Do not copy the intro verbatim.

### 4. Find a hero image

Look in each source file for a body image: `![alt](/assets/....png)` (or `.jpg`), often with `{: .zoomable }`, or an Excalidraw diagram PNG in `docs/assets/`.

Ignore:
- the inline H1 logo (`<img ... style="height:1em ...">`),
- decorative images with `alt=""` inside custom widgets.

If one or more posts have a real image, pick the single best one (a diagram beats a screenshot beats a logo) and name its file path for the user to attach. LinkedIn cannot embed it by URL, the user drags the file in.

### 5. Hand back the block

Print the fenced text block in chat, then the `Attach:` line (or the "no strong image" note) underneath it.
Do not run `git`, do not edit any post, do not post anywhere.

## Worked example

Two likes, codeburn and peon-ping, neither has a body image (logos only). This is the real post that shipped:

```
Hey all, I have another small blog update.
Dutch follows English.
I would like to share two tools I recently added to my AI Coding stack with you:
- CodeBurn: https://blog.ramseskools.nl/likes/codeburn/
- peon-ping: https://blog.ramseskools.nl/likes/peon-ping/

CodeBurn lets me track how many tokens my AI coding agents burn and spot where to optimize, all local and private.

peon-ping lets my AI coding agents ping me with iconic game voice lines and a desktop banner when they finish, hit an error, or need my input.

Hoi allemaal, weer een kleine blog update.
Ik wil twee nieuwe tools delen die ik recent aan mijn AI Coding stack heb toegevoegd:
- CodeBurn: https://blog.ramseskools.nl/likes/codeburn/
- peon-ping: https://blog.ramseskools.nl/likes/peon-ping/

Met CodeBurn zie ik hoeveel tokens mijn AI coding agents verbruiken en waar ik kan optimaliseren, volledig lokaal en privé.

Met peon-ping pingen mijn AI coding agents me met vette game voice lines en een desktopmelding als ze klaar zijn, vast lopen, of mijn input willen.
```

No strong image on either post, so nothing to attach.
