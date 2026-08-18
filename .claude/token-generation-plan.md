## Plan: Agent Throughput Post + Interactive Session Demo

Publish a post that reframes performance from raw token/sec to agent-task throughput, backed by local session evidence and an interactive mock session player. Use a dual-track dataset: extract measurable real metrics from local logs where available, and explicitly mark unobservable metrics as estimated or unavailable. Ship the article and demo together in one release.

**Steps**
1. Define the metric framework and claims boundary.
- Create a short metric taxonomy with three buckets:
  - Model generation metrics: output tokens, estimated token/sec, thinking-related token counters when available.
  - Agent workflow metrics: iterations, tool calls by type, file reads, file edits, elapsed wall-clock per task.
  - Outcome metrics: time-to-first-useful-output and time-to-complete-task.
- Define what is measured vs inferred vs unavailable, and use this legend consistently in text, charts, and demo UI.
- Dependency: none.

2. Build a local session extraction pipeline for reproducible evidence.
- Add a small extractor under docs/assets/agent-session-demo/tools to parse local sessions into normalized JSON.
- Claude source path support:
  - Parse local Claude JSONL sessions for per-message usage fields, model identifiers, tool-use events, and timestamps.
  - Compute: iterations, total/avg input-output tokens, tool call counts by tool name, file operations, total elapsed time.
- Copilot source path support:
  - Parse available session metadata and turn/file references to compute: turns, file references, coarse timings.
  - Include optional hooks for richer telemetry if present, but tolerate missing token-level fields.
- Output one normalized schema per session into docs/assets/agent-session-demo/data/derived.
- Dependency: step 1.

3. Curate redacted showcase sessions from real data.
- Select 3-5 representative sessions from both tools:
  - quick fix,
  - medium refactor/investigation,
  - longer multi-tool task.
- Create curated session files in docs/assets/agent-session-demo/data/sessions as human-editable JSON (or YAML if preferred), preserving event sequence while redacting sensitive text/paths.
- Add metadata fields for story labels (for example: “fast token stream, slow task progress” vs “moderate token stream, high task throughput”).
- Dependency: step 2.

4. Compute derived metrics and caveated token/sec views.
- Add a lightweight transformer that calculates per-session KPIs:
  - elapsed seconds,
  - event counts by category,
  - file-read/file-edit counts,
  - turns/iterations,
  - tokens where present.
- For token/sec:
  - Use direct calculation only when both token counts and elapsed model-response interval are available.
  - Else mark token/sec as estimated or unavailable with reason.
- Generate comparison summaries consumed by both article visuals and interactive demo.
- Dependency: steps 2-3.

5. Build the static interactive “agent session player”.
- Follow the existing embed pattern used by the logo generator:
  - self-contained HTML app plus JS/CSS assets under docs/assets/agent-session-demo,
  - embedded in post via iframe.
- Player capabilities:
  - choose predefined sessions,
  - scrub through timeline events,
  - display per-step event type, timestamp deltas, tool/file activity, token counters,
  - slider to vary token/sec and replay text emission speed,
  - side-by-side view of “token stream speed” versus “task progress speed.”
- Include a compact legend showing measured/inferred/unavailable statuses.
- Dependency: steps 3-4.

6. Write the post narrative around evidence and demo.
- Create a new post in docs/posts with:
  - clear thesis: token/sec alone is insufficient for agentic coding productivity,
  - method section: local data sources, normalization, caveats,
  - findings section: where token speed correlates weakly/strongly with task throughput,
  - interactive section: iframe to the session player,
  - practical recommendations for evaluating models in agent harnesses.
- Include a <!-- more --> marker with a concise intro optimized for hover preview.
- Dependency: steps 1-5.

7. Integrate build flow and publishing checks.
- Add a simple command path (manual or script) to refresh derived session data before publishing.
- Verify MkDocs build and local rendering of iframe asset paths.
- Run privacy audit on curated data files before release.
- Dependency: steps 2-6.

8. Optional follow-up hardening (parallel after release).
- Add a documented “capture protocol” for future sessions so metrics are more complete over time.
- Add richer charts if later telemetry includes stable model-side latency/token details.
- Dependency: after step 7; can run in parallel with future posts.

**Relevant files**
- /Users/ramses.kools/private_workspace/my-blog/docs/posts — add the new article markdown and keep style/frontmatter consistent with existing posts.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/logo-generator/logo-generator-embed.html — reference pattern for self-contained iframe app structure.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/logo-generator/assets/logo-engine.js — reference pattern for reusable pure logic module used by embed UI.
- /Users/ramses.kools/private_workspace/my-blog/docs/posts/logo.md — reference pattern for embedding iframe in post content.
- /Users/ramses.kools/private_workspace/my-blog/blog_hooks.py — optional extension point if you later want post-build generation of demo data artifacts.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/custom.css — optional shared styling hooks if you want visual alignment with site design.
- /Users/ramses.kools/private_workspace/my-blog/mkdocs.yml — verify current asset handling and any future plugin/watch additions.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/tools (new) — extractor/transform scripts.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/data/sessions (new) — curated editable session definitions.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/data/derived (new) — generated normalized metric outputs.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/agent-session-embed.html (new) — interactive demo UI host.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/agent-session-player.js (new) — timeline/player logic.
- /Users/ramses.kools/private_workspace/my-blog/docs/assets/agent-session-demo/agent-session.css (new) — demo-specific styling.

**Verification**
1. Data completeness validation.
- Run extractor against at least one Claude and one Copilot session.
- Confirm schema fields populate correctly and missing fields are tagged as unavailable, not silently zeroed.
2. Metric correctness spot checks.
- Manually verify 2-3 sessions for: tool call counts, file read/edit counts, elapsed duration.
- Verify token/sec derivation only appears where required raw values exist.
3. Privacy checks.
- Confirm curated session files contain no sensitive names, repository internals, or absolute local paths.
4. UX behavior checks.
- Validate session switching, timeline scrubbing, and token/sec slider behavior on desktop and mobile.
- Ensure iframe loads correctly from post page with absolute asset paths.
5. Content checks.
- Confirm thesis, caveats, and measured-vs-inferred legend appear in both article and demo.
- Confirm <!-- more --> marker placement gives a clean hover preview snippet.
6. Build checks.
- Run local mkdocs build/serve and verify no broken asset links or JS errors for demo assets.

**Decisions**
- Include lightly redacted real examples rather than fully synthetic-only sessions.
- Ship article and interactive demo in the same release.
- Include token/sec where possible, but always caveated and clearly marked as measured, estimated, or unavailable.
- In scope: local-session evidence from Claude and Copilot artifacts that are practically accessible now.
- Out of scope (for this release): guaranteed model-provider ground-truth latency internals where local logs do not expose them.

**Further Considerations**
1. Session format choice recommendation.
- Option A: JSON only for simplest browser loading.
- Option B: YAML authoring + build conversion to JSON for better manual editing.
- Recommendation: start with JSON for release 1, add YAML authoring later only if editing friction appears.
2. Visual emphasis recommendation.
- Keep one prominent chart that compares token stream speed vs task progress speed over time.
- Avoid many micro-metrics in release 1 to keep the thesis clear.
3. Future comparability recommendation.
- Add a lightweight session metadata block (tool version, model, date, task type) so future posts can compare trends across months.
