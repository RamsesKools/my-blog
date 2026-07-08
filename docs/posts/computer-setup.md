---
date: 2026-07-08
slug: computer-setup
---

# Setting up my new macbook from a repo

I recently got a new MacBook for work.
Normally that means days of reinstalling apps, digging up settings, and slowly rediscovering all the little tweaks I forgot I made.
This time I did it differently: I turned my old machine's configuration into a repo, and installed the new machine from that.
This post is about that repo, why I think this is worth doing, and how the setup works.

<!-- more -->

## The problem with configuring by hand

Over the years I have accumulated a lot of configuration: shell aliases, git settings, keyboard bindings, mouse tweaks, VS Code settings, macOS preferences, and lately also configuration for AI coding agents.
Each of those was a small decision I made once, and each one makes my machine feel more personalized.

The trouble is that all of it lived on one laptop.
Every new machine meant reconstructing that from memory, and my memory is really not good enough for this.
The same annoyance shows up with AI agents: without a proper global agent context, you end up re-explaining your preferences to every agent in every repo.
That part got its own repo and [its own post](agent-config.md).

The dotfiles crowd solved this a long time ago.
[dotfiles.github.io](https://dotfiles.github.io/) collects the community wisdom, and puts it nicely: "Your dotfiles might be the most important files on your machine."
My setup is heavily inspired by [driesvints/dotfiles](https://github.com/driesvints/dotfiles), which takes the idea beyond dotfiles into a full machine bootstrap.

## Why a setup repo

Four reasons convinced me this is worth the effort.

1. **Configuration is accumulated craft.**
Those years of tweaks are real invested knowledge.
Without a repo they silently live on one machine, and they get lost or half-remembered when that machine goes away.
Putting them in git makes the craft durable.
2. **Machines stay in sync.**
The repo does not copy config files to their destination, it symlinks them.
Edit an alias on one machine, commit, pull on the other, done.
One source of truth instead of slowly diverging copies.
3. **A fast, calm reinstall.**
A new (or wiped) machine goes from unboxing to fully-mine by running one script.
The script is idempotent, so if something fails halfway I just run it again.
No days of "oh right, I also need...".
4. **The repo doubles as documentation, and agents can read it.**
Every tool I use is listed in a `Brewfile` or a plain text list.
That is documentation as a side effect, for me and for my AI coding agents.
Claude Code helped me build the scripts, and because everything is enumerated in the repo, it can later help me port the whole thing to Windows.

## What's in the repo

The repo lives at `~/.dotfiles` and looks like this:

```text
fresh.sh              bootstrap script — run once on a new Mac
verify.sh             check all tools are installed correctly

Brewfile              Homebrew formulae and casks
lists/                VS Code extensions, npm globals, pipx tools (one per line)
workspaces/           repo lists per workspace (private, work, ...)
scripts/              helpers: SSH keys, extension installs, workspace cloning

zsh/                  shell config (.zshrc, .zshenv, aliases, path)
git/                  .gitconfig and global gitignore
ssh/                  SSH host config (no private keys!)
vscode/               VS Code settings and keybindings
keyboard/             macOS key binding overrides
config/               tool configs (linearmouse, gh CLI)
macos/                macOS system preference scripts
apps/                 docs for apps that need manual install or sign-in
```

A few patterns worth pointing out:

- **Plain text lists** drive the installs.
Adding a VS Code extension to the setup means adding one line to `lists/vscode-extensions.txt`.
Simple to maintain, trivial to diff, and easy for an agent to read.
- **Workspace repo lists** describe which repositories get cloned where.
One list per context, so my personal projects and each work context land in their own workspace folder.
- **Docs for the unautomatable.**
Some things resist scripting: App Store installs, VPN clients from IT, apps that need a manual sign-in.
Those get a markdown file in `apps/` instead of a script, so at least the checklist is versioned.

## fresh.sh: one script to set up the machine

The heart of the repo is `fresh.sh`.
It walks through the whole setup interactively and is safe to re-run: every step checks before acting.

1. Xcode CLT + SSH keys
2. Oh My Zsh + Homebrew
3. `brew bundle`: all formulae and casks
4. VS Code extensions
5. Symlink dotfiles into place
6. Runtimes: Node, Python, Bun
7. Clone `~/.agents` + run its symlink setup
8. Clone all workspace repos
9. macOS preferences
10. `verify.sh` + manual steps checklist

The symlinking step is where the "machines stay in sync" magic happens.
A small `link()` helper points `~/.zshrc`, `~/.gitconfig`, VS Code settings, and friends back at the repo.
If a real file already exists at the target, it is backed up to a timestamped folder first, so the script never destroys anything.

At the end, `fresh.sh` prints a checklist of the manual steps that cannot (or should not) be automated: signing in to CLIs, copying private SSH keys, granting macOS permissions to background apps, migrating browser profiles.
Then `verify.sh` runs through every tool and prints `[ok]` or `[fail]` per check, with a pass/fail summary at the end.
That last part turned out to be surprisingly satisfying: a green summary and you know the machine is ready.

## Keeping it alive

A setup repo only works if it stays current, so the real trick is a habit:

- New Homebrew package? Add it to the `Brewfile`.
- New VS Code extension or CLI tool? Add it to the list in `lists/`.
- Shell or git tweak? Edit the file in the repo, since the live file is a symlink anyway.
- Commit and push, so every future machine gets it for free.

The symlinks do most of the heavy lifting here.
Because the live config files literally are the repo files, day-to-day tweaking keeps the repo up to date almost automatically.

## Deliberately not perfect

Earlier attempts at this kind of thing taught me that aiming for the perfect setup repo is a great way to never finish one.
So this iteration has explicit limitations:

- **macOS only, for now.**
I also have two Windows machines, so a Windows adaptation is likely next.
The groundwork is done: the `Brewfile` and the lists document every tool, so writing equivalent install scripts is mostly translation work.
- **Known issues.**
The top issue for me for now is that the repo installs the GitHub CLI, but you need GitHub access to clone the repo.
A classic chicken-and-egg problem that is still on the TODO list.

The repo itself is private, because it contains work-specific workspace lists.
In the spirit of [building in public](blog-infrastructure.md) I published a depersonalized snapshot at [github.com/RamsesKools/macbook-setup-example](https://github.com/RamsesKools/macbook-setup-example).
I don't intend to keep that example very up to date, but it does show what my current setup looks like.

## The AI agent layer

One deliberate design decision: configuration for AI coding agents (Claude Code, Codex, GitHub Copilot CLI) lives in its own `~/.agents` repo, not in the dotfiles.
`fresh.sh` clones it and runs its symlink setup as one of the steps, but the content evolves on its own rhythm.
How that works, and why one file can configure three different agents, is the subject of [the next post](agent-config.md).
