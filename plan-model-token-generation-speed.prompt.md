## Plan: Agent Throughput + Token Speed Post and Demo

Goal: publish one cohesive release that proves why raw token/sec is not enough for agentic coding, while still showing provider/model token speed as one useful (but limited) dimension.

Current branch for all work below: `feat/agent-throughput-token-speed`.

## Working Principles

- Keep all implementation, data curation, and writing on the dedicated branch until ready for review.
- Explicitly label every metric as: measured, estimated, or unavailable.
- Prefer real session evidence first, then estimation fallback only where direct telemetry is missing.
- Maintain privacy by light redaction of sensitive paths, project names, and payloads.

## Workstream 1: Investigation into local sessions (evidence foundation)

Objective: extract what can actually be measured from local Claude Code, Codex, and GitHub Copilot session artifacts.

### 1.1 Inventory and schema mapping
- Identify local data sources per agent/tool.
- Document which fields are present for:
  - timestamps,
  - request/response boundaries,
  - usage tokens,
  - tool calls,
  - file reads/edits,
  - model identifiers.
- Produce a capability matrix per platform (Claude Code, Codex, Copilot).

### 1.2 Normalized extractor
- Build a small extractor under `docs/assets/agent-session-demo/tools`.
- Parse local session data into one normalized JSON schema under `docs/assets/agent-session-demo/data/derived`.
- Ensure missing metrics are stored as `null` with a reason tag, never silently defaulted to zero.

### 1.3 Derived metrics from real sessions
- Compute per session:
  - wall-clock duration,
  - time to first useful output event,
  - iteration count,
  - tool-call counts by type,
  - file-read/file-edit counts,
  - token metrics where available.
- If possible, compute:
  - TTFT (time to first token),
  - output token/sec.
- When impossible from artifacts, mark unavailable and explain why.

### 1.4 Curated showcase data
- Select 3-5 representative sessions across tools and task sizes.
- Create lightly redacted curated session files under `docs/assets/agent-session-demo/data/sessions`.
- Keep sequence and timing fidelity while redacting sensitive details.

Deliverables:
- Capability matrix for session telemetry.
- Normalized derived session JSON files.
- Curated redacted session fixtures for the visualizer.

## Workstream 2: Investigation into model-provider token speed

Objective: provide a separate, transparent view of provider/model token delivery speed to complement agent-level throughput.

### 2.1 Provider/model scope
- Compare at least:
  - Claude Code (including Fast Mode context and caveats),
  - Codex,
  - GitHub Copilot chat/agent paths,
  - multiple models where selectable.
- Include explicit note: Claude Fast Mode policy/behavior exists, but published docs do not provide direct per-request speed guarantees.

Reference:
- https://code.claude.com/docs/en/fast-mode#enable-fast-mode-for-your-organization

### 2.2 Measurement strategy (priority order)
1. Direct telemetry from real session logs:
- Use request timestamps + usage counters if present to compute TTFT and token/sec.
2. Controlled local benchmark prompts:
- Generate long deterministic outputs and measure elapsed response stream timing.
- Use provider-reported token counts when available.
3. Estimation fallback:
- If token counts are absent, estimate from text using tokenizer approximations.
- Mark as estimated and lower-confidence.

### 2.3 Caveats and quality grading
- For each metric result, attach quality grade:
  - High: direct measured tokens + timing,
  - Medium: partial telemetry + constrained assumptions,
  - Low: rough text-to-token estimate.
- Include explicit warning that text-length conversion is a weaker method.

Deliverables:
- Provider/model token-speed comparison table (with confidence grade).
- Clear methodology note distinguishing measured vs estimated.

## Workstream 3: Agent-session-token-speed visualizer

Objective: interactive static demo showing why token speed and task throughput diverge.

### 3.1 App structure
- Build self-contained assets under `docs/assets/agent-session-demo/`:
  - `agent-session-embed.html`,
  - `agent-session-player.js`,
  - `agent-session.css`,
  - data files in `data/sessions` and `data/derived`.
- Embed from blog post via iframe.

### 3.2 Core interactions
- Session picker for default curated sessions.
- Timeline scrubber over step events.
- Event stream panels:
  - prompt,
  - thinking,
  - tool calls,
  - file reads/edits,
  - response chunks.
- Configurable token/sec slider to simulate text emission speed.
- Side-by-side indicators:
  - token stream speed,
  - task progress speed.

### 3.3 Visual metrics and legend
- Show TTFT, token/sec, duration, tool activity, and iteration depth.
- Display measurement status badges: measured / estimated / unavailable.
- Mobile and desktop responsive behavior.

Deliverables:
- Production-ready static visualizer embed.
- Preloaded representative sessions.

## Workstream 4: Blog post itself

Objective: publish the narrative and evidence with the visualizer in one release.

### 4.1 Post narrative structure
- Thesis: token/sec is only one layer; agent throughput is what impacts real programming productivity.
- Method: how session and provider investigations were done.
- Findings:
  - where token speed matters,
  - where it does not predict total task latency.
- Practical model/tool evaluation checklist for daily AI-assisted programming.

### 4.2 Content requirements
- Include iframe demo section.
- Include provider token-speed section with caveats.
- Include `<!-- more -->` marker early for hover preview quality.
- Keep concise style aligned with repository writing conventions.

Deliverables:
- New post markdown under `docs/posts/`.
- Embedded demo and supporting assets linked correctly.

## Integration, validation, and release

### Validation checklist
1. Extraction validation:
- At least one verified session per platform path used.
- Schema fields validated for nullability and reason tags.

2. Metric validation:
- Manual spot checks for duration, tool counts, and token/sec math.

3. Privacy validation:
- Curated files contain no sensitive names/absolute local paths.

4. UI validation:
- Demo works in `mkdocs serve` on desktop and mobile layouts.

5. Build validation:
- `uv run mkdocs build` passes with no broken asset links.

### Release flow
- Keep all commits on `feat/agent-throughput-token-speed`.
- Open PR when:
  - all four workstreams are complete,
  - caveats are explicit,
  - visualizer and post are both ready.

## File map

Existing references:
- `docs/posts/logo.md`
- `docs/assets/logo-generator/logo-generator-embed.html`
- `docs/assets/logo-generator/assets/logo-engine.js`
- `mkdocs.yml`
- `blog_hooks.py`

Planned additions:
- `docs/assets/agent-session-demo/tools/*`
- `docs/assets/agent-session-demo/data/sessions/*`
- `docs/assets/agent-session-demo/data/derived/*`
- `docs/assets/agent-session-demo/agent-session-embed.html`
- `docs/assets/agent-session-demo/agent-session-player.js`
- `docs/assets/agent-session-demo/agent-session.css`
- `docs/posts/<new-post>.md`

## Open risks

- Some platforms may not expose token timing artifacts needed for strict TTFT/token/sec.
- Tokenization-based estimation can be directionally useful but lower confidence.
- Cross-tool comparisons can be biased by differing session formats and buffering/streaming semantics.

Mitigation:
- Separate measured and estimated results clearly.
- Publish confidence grades with every speed number.
