---
date: 2026-08-31
slug: peon-ping
tags:
  - Tools
  - AI
---

# <img src="/assets/peon-ping.png" alt="peon-ping logo" style="height:1em; vertical-align:middle; display:inline;"> peon-ping

[peon-ping](https://github.com/PeonPing/peon-ping) allows you to play an iconic game voice line and pop a desktop banner when your AI coding agent finishes a task, hits an error, or needs your input.
There is a whole [site](https://www.peonping.com/) with [many different sound packs available](https://openpeon.com/packs) for it now, but at heart it is a small tool that allows your agent to communicate sounds and notifications.

<!-- more -->

## Hear a peon

The name comes from the Warcraft III Orc Peon.
My own default is the StarCraft SCV.
Hit a line to hear what both packs sound like.

<div class="peon-demo">
  <p class="peon-demo-label"><img src="/assets/peon-ping.png" alt="">Warcraft III Orc Peon</p>
  <div class="peon-demo-buttons">
    <button type="button" data-src="/assets/peon-ping-sounds/ready-to-work.mp3">Ready to work?<span>session start</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/work-work.mp3">Work, work.<span>task picked up</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/something-need-doing.mp3">Something need doing?<span>needs input</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/hmm.mp3">Hmm?<span>needs input</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/not-that-kind-of-orc.mp3">Me not that kind of orc!<span>error</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/me-busy.mp3">Me busy, leave me alone!<span>too many pings</span></button>
  </div>
  <p class="peon-demo-label"><img src="/assets/scv-ping.png" alt="">StarCraft SCV</p>
  <div class="peon-demo-buttons">
    <button type="button" data-src="/assets/peon-ping-sounds/scv-good-to-go.mp3">SCV good to go, sir<span>session start</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/scv-jobs-finished.mp3">Job's finished<span>task done</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/scv-yes-sir.mp3">Yes, sir?<span>needs input</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/scv-orders-capn.mp3">Orders, Cap'n?<span>needs input</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/scv-somethings-in-the-way.mp3">Somethin's in the way<span>error</span></button>
    <button type="button" data-src="/assets/peon-ping-sounds/scv-claustrophobic.mp3">They put me in one of these things!<span>too many pings</span></button>
  </div>
</div>

<script>
(function () {
  var root = document.currentScript.previousElementSibling;
  var audio = new Audio();
  [].forEach.call(root.querySelectorAll('button[data-src]'), function (btn) {
    btn.addEventListener('click', function () {
      audio.pause();
      audio.src = btn.dataset.src;
      audio.currentTime = 0;
      audio.play();
    });
  });
})();
</script>

Sounds from the `peon` and `sc_scv` packs ([openpeon.com](https://openpeon.com/packs)).

## The problem I was having

I kept running into the same thing:
I would give a coding agent inside VS Code a big instruction, expect it to work for a few minutes, and in the mean time I would move my attention to another window.
Then I would come back later and find it had stalled thirty seconds in, waiting on input.

At some point I just told the agent: "ping me if you need me."
But, it had no way to do that just yet.
So I went looking for a tool to allow my coding agent to "ping me"m, I found peon-ping, and the 90s gaming sound packs I recognized made me love it instantly.
Now when I tell an agent to turn on alerts, it actually can.

## How I have it wired up

I use it with the two agent harnesses I work in most, Claude Code and GitHub Copilot CLI, both through their hook systems.
The binary comes in through my [[computer-setup|dotfiles]] as a Homebrew tap, so a fresh laptop gets it automatically.

On top of that I built a small custom layer in my [[agent-config|agents config repo]]:

- One `alert-me` skill instead of juggling separate commands, so any agent triggers it the same way.
- A gate in front of every hook event, so only sessions that opted in make noise and every other agent stays silent. Subagent events are dropped entirely.
- A CLI path (`alert.sh done -m "..."`), which is handy when I want the agent to ping me halfway through a plan, not only when the whole turn ends.

It sends both an audio clip and a desktop notification.
The overlay banner shows the repo name and which harness it is, like `.agents - Claude Code`, so parallel agents stay distinguishable.

## Personalizing each agent

peon-ping ships 165+ sound packs pulled from games like Warcraft III, Red Alert 2, StarCraft II, and Counter-Strike.
I decided I wanted my agents to feel a little distinct, so I set the pack per project and per session.
My default is the StarCraft SCV, and I rotate through a handful that all point at other things I like: Jarvis from Iron Man, GLaDOS from Portal, the Red Alert 2 SCV and Tanya, and the Warcraft III Peon.

There is an MCP server too, but I steer away from MCP in general because it is too token-hungry for my taste, so the per-session voice switching is something I wired up myself instead.

It is still quite a new project, but I expect I will be spreading the love on this one the same way I do with [[clipboard-history|clipboard history]].
