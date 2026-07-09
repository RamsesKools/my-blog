---
date: 2026-05-19
tags:
  - Design
  - Tools
---

# Creating my own logo

Designing a personal logo turned into its own little journey.
Nowadays it is easier than ever to generate a quick logo using a text-to-image model.
But I didn't really like that approach.
I wanted something recognizable, simple, minimalistic, focused on content, and reproducible from configuration.

<!-- more -->

## The design

I started working on my design and thinking about colors, fonts, animations, and more.
My primary blue color was something that I choose quickly: it is the clothing color I had in my [board year of my study association](https://acdweb.nl/bestuur/oud).
I wanted something that fits with my personality and becomes easily recognizable.

After a weekend of thinking about it, inspiration hit me when I saw the very recognizable logo of Tommy Hillfiger on the back of some jeans.
It hit me that the two boxes next to each other where enough to recognize the brand.
At the same time you can add text inside.
In the end I only really kept the two boxes from that idea, and started tinkering with it further by myself.

I ended up choosing a simple design: my initials in my own font, both in a rounded square box, sitting side by side.
One letter sits on a white or transparent background, the other on my primary accent blue.
The boxes themselves carry the opposite color, with a primary blue outline tying them together.

![RK logo](/assets/logo-rk.svg)

The result is something I can recognize at a glance, that fits the rest of my personal design system, and that scales cleanly from a favicon to a bigger image.

## SVG, always

I decided pretty quickly that [SVG](https://en.wikipedia.org/wiki/SVG) is the best format for my logo, and honestly for any logo.
It scales without losing quality, it's small, it's text, and it can be styled or themed via CSS.
Raster formats like PNG are fine for export, but the source of truth should always be vector.

## A logo generator

Rather than hand-tweaking SVG paths, I decided to write a tool to generate the logo for me.
After an afternoon of tinkering I had a [logo generator](https://ramseskools.nl/logo-generator.html) that fit my needs and let me fine-tune every property: colors, font, box sizes, corner radius, stroke width, alignment, padding.

The generator gave me a live preview and export to SVG, PNG, or a YAML snippet for my config.
From the same generator I could produce my `[R|K]` logo, but also page-titles in the same style: `[Ramses|Kools]`, `[home|server]`, `[logo|generator]`, and so on.
That turned out to be the unlock: one tool, one visual language, many logos.

![ramses.kools logo](/assets/logo-ramseskools.svg)
![home.server logo](/assets/logo-homeserver.svg)
![logo.generator logo](/assets/logo-generator.svg)
{: .image-row }

## CLI for batch generation

I also wanted the generator to work as a CLI script that reads a config file.
The idea was that if I ever change my color, font, or any other property about my logo, I can quickly recreate all logos in the new style and replace the old ones in one go.

This might have been a bit of over-engineering, since I was solving future problems that may never happen.
But it kept the design system honest: every logo is just a row in a YAML file, not a hand-crafted asset that drifts over time.

## Try it yourself

Below is a slimmed-down version of the generator, embedded right here.
Pick two colors, type your initials, and download the result.

<!-- markdownlint-disable MD033 -->
<iframe
  src="/assets/logo-generator/logo-generator-embed.html"
  title="Logo generator"
  loading="lazy"
  style="width:100%;border:0.5px solid #e5e5e5;border-radius:4px;height:320px;"></iframe>
<!-- markdownlint-enable MD033 -->
