---
date: 2026-06-03
tags:
  - Design
  - Tools
---

# How I created my personal design

For my blog, but also for every other front-end, website, or little tool I build, I wanted one personal style: a logo, colors, a font, animations, and a general look and feel.
The nice bonus: once it is written down, my AI coding agents can read it and generate slides, websites, and UI that already look like me.
This post is about how I created that style.

<!-- more -->

## Why a personal style

The simple reason is recognizability and personalization.
When my blog, my homepage, and my little side tools all share the same colors, font, and logo, they start to feel like one thing instead of a pile of unrelated projects.
It gives everything a bit of personality, and it makes my work recognizable as mine at a glance.

There is a second reason that turned out to matter even more lately: it keeps AI-generated output from looking generic.
These days I let coding agents generate a lot of the visual work, slide decks, websites, front-end UI, diagrams, icons, and left to their own defaults they all come out in the same bland, off-the-shelf style.
A written-down style fixes that, which is what the [DESIGN.md](#designmd) section below is all about.

## A color palette from a photo

The [coolors.co palette generator](https://coolors.co/) did most of the heavy lifting here.
You can see my palette in it directly: [coolors.co/70ae6e-3e77dc-f8f7f6-1b2629-f29559](https://coolors.co/70ae6e-3e77dc-f8f7f6-1b2629-f29559).

My signature blue came from a real place: the clothing color my study association board picked for [our board year (ACD board #69, 2014-2015)](https://acdweb.nl/bestuur/oud).
When we shot our board pictures in those new clothes, I remember one nice photo in front of some trees and buildings.
So I used that image and pulled the rest of the palette straight out of it: the green from the leaves, an off-white from the building, and the blue from our shirts.

From there coolors makes it easy to derive lighter and darker accent tones, and I used it again to pick the supporting semantic tokens like warning and danger.
For me the process went like this:

1. Extract some colors from the image
    - You can upload the image directly to coolors.co, or you can just use some color-picker tool.
    - I used the [Raycast color picker tool](https://www.raycast.com/thomas/color-picker).
2. Put the colors in coolors.co, and create variants.
    - Lighter and darker tones.
    - Lock your primary colors and then use the spacebar to generate new colors that fit together until you find some that you like.
        - This is how I found the orange/red colors that fit nicely into my design.
3. Add these colors to a `.css` file and create a preview `html` page.
4. Tweak the colors until I like how it looks.

The result is a small set of brand and semantic tokens I can now use for all my designs:

<!-- markdownlint-disable MD033 -->
<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:1em 0;">
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#3E77DC;color:#fff;font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(255,255,255,0.22);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-blue</code>#3E77DC</span>
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#70AE6E;color:#fff;font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(255,255,255,0.22);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-green</code>#70AE6E</span>
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#F8F7F6;color:#1B2629;border:1px solid rgba(27,38,41,0.18);font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(27,38,41,0.08);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-bg</code>#F8F7F6</span>
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#1B2629;color:#fff;font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(255,255,255,0.22);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-dark</code>#1B2629</span>
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#F29559;color:#fff;font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(255,255,255,0.25);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-warning</code>#F29559</span>
  <span style="display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;background:#F55D3E;color:#fff;font-family:monospace;font-size:13px;line-height:1.4;"><code style="background:rgba(255,255,255,0.25);padding:1px 6px;border-radius:5px;color:inherit;font-size:inherit;">--c-danger</code>#F55D3E</span>
</div>
<!-- markdownlint-enable MD033 -->

## More than colors and a logo

A palette and a logo are the recognizable bits, but a style is more than that.
A few other things go into mine:

- **Fonts**: a clean sans for text and a monospace for labels and code, which gives it a subtle engineering feel.
- **Look and feel**: light-mode, lots of whitespace, restrained but human, with the blue accent doing the heavy lifting.
- **Animations**: small and quick, gentle hover transitions and a smooth scroll, nothing flashy.
- **UI rules**: tight corner radii, thin borders, and consistent spacing so components feel like one set.

Each of these is just another decision to write down once and reuse everywhere.

## DESIGN.md

All of that only helps the AI agents if I can actually hand it over.
The trick is putting the whole style in a single file the agent reads before it generates anything.

[`DESIGN.md`](https://github.com/google-labs-code/design.md) is the emerging standard for exactly this.
It is an open-source format from Google Labs that pairs machine-readable design tokens (colors, type, spacing, radii in YAML) with human-readable prose explaining how to use them.
Any agent that follows [`AGENTS.md`](https://agents.md/) cross-references (Claude Code, Codex, Cursor, and others) can read it and generate UIs that match your style instead of inventing a new one each time.

### Creating DESIGN.md

I did not write mine from scratch.
I opened a [claude.ai](https://claude.ai) chat, said I wanted to work together on deciding my style, and asked it to interview me first and show the effect of my choices live.
That one instruction, ask questions before building, shaped the whole session.
You can read [the full conversation here](https://claude.ai/share/6ac6191e-d04e-444a-86b2-3fe347a52006).

It played out in three phases:

1. **Vibe and direction.** Broad questions first: overall feel, aesthetic references, what impression I want to leave. My answers landed on clean, minimal, engineering-flavored, restrained but human.
2. **Design specifics.** Then it narrowed in on color temperature, the role of the accent, typography, spacing density, and corner radius. This is where I fed in my palette and made concrete calls.
3. **Identity details.** Finally the name format, tagline, and which page sections to include. With all of that, Claude built a full live preview in one shot.

From there I kept iterating: adding the semantic tokens, splitting the single artifact into a proper `index.html` plus `style.css`, and generating a `DESIGN.md` that documents everything so the system is reproducible and version-controllable.
Every time I changed the CSS and liked the result, I had Claude update the `DESIGN.md` based on that decision.
This loop (generate, tweak, promote the change back into the spec) keeps running, and it is what makes the document actually mine rather than a generic template.

It also ties back to my [logo generator](logo.md): the logo, the palette, and the `DESIGN.md` are all just configuration now, so every new thing I build starts out already looking like me.
