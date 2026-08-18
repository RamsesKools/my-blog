# Token generation speeds across model providers

A snapshot of output token speed (tokens/sec, after the first token arrives) across the big model providers and the hyperscaler platforms that host their models, plus a look at the "faster" tiers some of them sell.

## Caveats before trusting any of this

- Numbers below are single-request, non-batched output speed unless noted. Concurrency, prompt length, reasoning/thinking effort level, region, and time of day all move these numbers a lot.
- Very few providers publish raw tokens/sec officially. Most figures here come from individual model pages on [Artificial Analysis](https://artificialanalysis.ai/leaderboards/models), which independently benchmarks the same model across every hosting provider that serves it, refreshed continuously. Where a number is pulled from AA's aggregated leaderboard view rather than a specific model's own provider page, that's noted — the leaderboard view is JS-rendered and less reliable to extract cleanly than a single model's page.
- This is a fast-moving space: model names below (GPT-5.6, Claude Opus 5, Mistral Large 3, Gemini 3.6) were current as of August 2026. Expect names and numbers to be stale within months.
- Independent hands-on tests (linked in [Further reading](#further-reading)) sometimes contradict vendor positioning by a wide margin. Treat every number here as directional.

## 1. Direct provider APIs, by model tier, latest generation

### OpenAI — GPT-5.6 family

| Tier | Model | Output speed | Source |
|---|---|---|---|
| Small / fast | GPT-5.6 Luna (max) | 244.0 t/s on Amazon Bedrock, 200.6 t/s on OpenAI direct | [AA: GPT-5.6 Luna](https://artificialanalysis.ai/models/gpt-5-6-luna/providers) |
| Large / flagship reasoning | GPT-5.6 Sol (max) | 55.0 t/s on OpenAI direct (only provider); (high) effort 61.3 t/s | [AA: GPT-5.6 Sol](https://artificialanalysis.ai/models/gpt-5-6-sol/providers) |

OpenAI's current naming (Luna/Sol) doesn't map cleanly onto a nano/mini/full size ladder the way GPT-5 did — Luna is the fast, cheap line and Sol is the flagship reasoning line. There's a real ~4x speed gap between them.

Model list: [platform.openai.com/docs/models](https://platform.openai.com/docs/models)

### Anthropic — current generation (Haiku 4.5, Sonnet 5, Opus 5)

| Tier | Model | Output speed | Source |
|---|---|---|---|
| Small | Claude Haiku 4.5 | 100.9 t/s (Amazon Bedrock), 90.8 (Google Vertex), 89.5 (Azure) | [AA: Claude 4.5 Haiku](https://artificialanalysis.ai/models/claude-4-5-haiku/providers) |
| Medium | Claude Sonnet 5 (max effort) | 85.1 t/s (Azure), 80.6 (Amazon), 78.2 (Anthropic direct) | [AA: Claude Sonnet 5](https://artificialanalysis.ai/models/claude-sonnet-5/providers) |
| Large | Claude Opus 5 (max effort) | 59.7 t/s (Google Vertex), 58.9 (Amazon), 53.5 (Anthropic direct) | [AA: Claude Opus 5](https://artificialanalysis.ai/models/claude-opus-5/providers) |

Worth flagging: on this generation, Haiku/Sonnet/Opus speeds are much closer together than the old "small is way faster" assumption suggests, and none of them is fastest on Anthropic's own API.

Model list: [platform.claude.com/docs/en/about-claude/models/overview](https://platform.claude.com/docs/en/about-claude/models/overview)

### Mistral — current generation (Small 4, Medium 3.5, Large 3)

| Tier | Model | Output speed | Source |
|---|---|---|---|
| Small | Mistral Small 4 | 166.8 t/s on Mistral's own API (only provider benchmarked) | [AA: Mistral Small 4](https://artificialanalysis.ai/models/mistral-small-4-non-reasoning/providers) |
| Medium | Mistral Medium 3.5 | ~97 t/s on Mistral's own API | [AA: Mistral Medium](https://artificialanalysis.ai/models/mistral-medium-3-5/providers) |
| Large | Mistral Large 3 | 139.1 t/s (Amazon Bedrock), 60.7 (Azure), 45.9 (Mistral direct) | [AA: Mistral Large 3](https://artificialanalysis.ai/models/mistral-large-3/providers) |

Model list: [docs.mistral.ai/models/overview](https://docs.mistral.ai/models/overview)

### Google Gemini — current generation (3.5 Flash-Lite, 3.6 Flash, 3.1 Pro)

| Tier | Model | Output speed | Source |
|---|---|---|---|
| Small | Gemini 3.5 Flash-Lite | 388.8 t/s (AA provider page), 350 t/s in Google's own pre-launch testing | [AA: Gemini 3.5 Flash-Lite](https://artificialanalysis.ai/models/gemini-3-5-flash-lite/providers), [AA article on the launch](https://artificialanalysis.ai/articles/gemini-3-6-flash-3-5-flash-lite-halving-time) |
| Medium | Gemini 3.6 Flash | 304 t/s in Google's/AA's pre-launch testing | [AA article on the launch](https://artificialanalysis.ai/articles/gemini-3-6-flash-3-5-flash-lite-halving-time) |
| Large | Gemini 3.1 Pro Preview | 135.4 t/s (Google AI Studio), 121.1 (Google Vertex) | [AA: Gemini 3.1 Pro Preview](https://artificialanalysis.ai/models/gemini-3-1-pro-preview/providers) |

Model list and pricing: [ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models), [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)

## 2. Cloud hyperscalers hosting the same models

AWS, Azure, and GCP mostly don't train their own frontier models (Gemini on Vertex is the exception — see below). They host Anthropic, Mistral, and OpenAI models on their own GPU fleets, and speed for the *same* model can differ meaningfully by host:

| Model | Amazon Bedrock | Google Vertex | Azure | Native/direct API |
|---|---|---|---|---|
| Claude Opus 5 (max) | 58.9 t/s | 59.7 t/s | not listed | 53.5 t/s |
| Claude Sonnet 5 (max) | 80.6 t/s | listed, exact figure not pulled | 85.1 t/s | 78.2 t/s |
| Claude 4.5 Haiku | 100.9 t/s | 90.8 t/s | 89.5 t/s | not in top 3 |
| Mistral Large 3 | 139.1 t/s | not listed | 60.7 t/s | 45.9 t/s |
| GPT-5.6 Luna (max) | 244.0 t/s | not applicable (not offered) | not listed | 200.6 t/s |

Sources: same AA provider pages linked in section 1.

### Where the coverage actually breaks down, and why

You asked me to be honest about gaps rather than force a comparison that doesn't exist. Here's the real picture:

- **Gemini has no cross-hyperscaler story at all.** It's Google's own model, so it's never offered on AWS or Azure. The only real comparison is Google's two own surfaces — AI Studio (consumer/direct) vs. Vertex AI (enterprise) — and even there AI Studio was faster in every case I found (135.4 vs 121.1 t/s on Gemini 3.1 Pro). There's no independent explanation for why; it could be routing overhead, a different fleet, or just noise on the day AA measured it.
- **Brand-new models lag on hyperscalers.** GPT-5.6 Sol, Mistral Small 4, and Mistral Medium 3.5 are all single-provider-only in AA's current data — no Bedrock, Azure, or Vertex listing yet. This tracks with how these deals work in practice: a hyperscaler has to certify and deploy a model on its own infra after the model vendor ships it, which typically takes weeks to months. If you need a model on Bedrock/Azure/Vertex specifically, the newest release from any given lab is the least likely one to be there yet.
- **Azure is thin on non-OpenAI/non-Anthropic coverage.** I found real Azure numbers for Claude and Mistral Large, but nothing for Gemini (expected, Google-only) and nothing yet for the newest GPT-5.6 models — despite Azure being OpenAI's own infrastructure partner, AA's tracked data hasn't caught up to the new model generation at the time of writing.
- **I could not find a credible source that isolates "hyperscaler overhead" from "different GPU generation/fleet."** When Bedrock beats a vendor's own API (Mistral Large 3: 139 vs 46 t/s), that's likely AWS running the model on newer or less-contended hardware, not some inherent Bedrock advantage — but no provider publishes fleet details, so this is inference, not a documented fact.

## 3. "Faster" tiers: separating hard numbers from vendor claims

Every major provider now sells some version of a speed/priority tier. The claims are easy to find; independent verification of those claims is not. Here's what I could and couldn't substantiate.

### What's independently corroborated

**Anthropic Fast Mode.** Anthropic's own docs claim "up to 2.5x higher output tokens per second" on Claude Opus 5 / Opus 4.8 (`speed: "fast"` beta parameter, still in research preview, $10/$50 per MTok in/out — see [docs](https://platform.claude.com/docs/en/build-with-claude/fast-mode)). Independent engineering analysis backs this up with a concrete before/after: [Sean Goedecke's technical breakdown](https://www.seangoedecke.com/fast-llm-inference/) estimates Opus going from ~65 t/s standard to ~170 t/s in fast mode — a ~2.6x jump, consistent with the official claim — and attributes it to running fast-mode requests in a much smaller batch (fewer concurrent sequences sharing a decode pass), possibly combined with speculative decoding. This is the best-substantiated "fast tier really works" claim I found across any provider.

### What's a vendor claim only, with no independent measurement found

- **OpenAI Fast Mode** (renamed from Priority Processing, July 30 2026): official claim is "up to 2.5x faster" per OpenAI's page, though a separate OpenAI FAQ says "up to 1.5x faster token velocity" for the same feature — the two OpenAI-published numbers don't even agree with each other. I searched specifically for independent before/after measurements (including a developer's hands-on writeup) and found none; the only real-world commentary I could find explicitly said the author had no empirical data of their own. Docs: [Fast mode overview](https://openai.com/api-fast-mode/), [FAQ](https://help.openai.com/en/articles/11647665-fast-mode-faq).
- **AWS Bedrock Priority tier**: AWS's own page states "up to 25% better output tokens per second (OTPS) latency compared to Standard tier" for supported models. I found no independent test measuring this delta. Docs: [Bedrock service tiers](https://aws.amazon.com/bedrock/service-tiers/).
- **AWS Bedrock latency-optimized inference** (the older, separate preview feature covering Claude 3.5 Haiku and Llama 3.1 70B/405B): AWS claims it "runs faster on AWS than anywhere else" but publishes no percentage, and I found no independent standard-vs-optimized comparison test. Docs: [latency-optimized inference](https://docs.aws.amazon.com/bedrock/latest/userguide/latency-optimized-inference.html).
- **Google Gemini Priority tier**: this is explicitly framed around reliability and queue priority, not speed — Google's docs don't publish an OTPS or latency percentage claim at all, and I found none independently either. Docs: [priority inference](https://ai.google.dev/gemini-api/docs/priority-inference).
- **Mistral**: has no dedicated speed/priority tier product as of this writing. Rate limits scale with plan tier, but Mistral doesn't throttle or accelerate per-token speed by tier.

### A different category entirely: dedicated fast models on dedicated hardware

**OpenAI's GPT-5.3-Codex-Spark** is not a toggle on an existing model — it's a distinct, smaller model that OpenAI built specifically for real-time coding and runs on Cerebras Wafer-Scale Engine silicon instead of Nvidia GPUs, OpenAI's first model to do so. This one does have a hard, independently reported number: [ServeTheHome](https://www.servethehome.com/openai-gpt-5-3-codex-spark-now-running-at-1k-tokens-per-second-on-big-cerebras-chips/) and [Cerebras' own post](https://www.cerebras.ai/blog/openai-codexspark) both put it at 1,000+ t/s, roughly 15x standard Codex's ~65 t/s. That's a genuinely verified number, but it's not a fair comparison to the "same weights, faster serving config" products above — you're getting a smaller/different model on different hardware, not the same model running faster. Currently a research preview limited to ChatGPT Pro users.

### The honest summary of section 3

Of five "faster tier" products from four providers plus Bedrock, only one (Anthropic's Fast Mode) has an independent measurement backing the vendor's number. Two providers' claims (OpenAI, AWS Bedrock Priority) are vendor-only, and OpenAI's own two published numbers for the same feature disagree with each other. Google's tier doesn't claim a speed benefit at all. Mistral has no such product. If you need this to actually be faster and not just marketed as faster, Anthropic's Fast Mode is the one claim I'd currently trust, and even that rests on one third-party blog post rather than a controlled benchmark.

## Further reading

Independent benchmarks and hands-on investigations, as opposed to vendor marketing pages:

- [Artificial Analysis — model & provider comparison](https://artificialanalysis.ai/leaderboards/models) — continuously refreshed, breaks output speed down per hosting provider for the same model. Source for most of the cross-host numbers above.
- [Sean Goedecke — Two different tricks for fast LLM inference](https://www.seangoedecke.com/fast-llm-inference/) — independent technical analysis of how Anthropic's and OpenAI's speed products actually work under the hood, with estimated before/after numbers.
- [5 LLM APIs Tested for Latency: Real Data (dev.to, March 2026)](https://dev.to/kunal_d6a8fea2309e1571ee7/5-llm-apis-tested-for-latency-real-data-2026-3e4o) — ran 5 major model APIs from a single server across three prompt sizes; found GPT-4.1 Mini running roughly 4x slower than Claude Haiku in practice despite being marketed as the lightweight option.
- [Avahi — Performance Testing AWS Bedrock Foundational Models](https://avahi.ai/case-study/performance-testing-aws-bedrock-foundational-models/) — load-tests Llama 3.3 70B on standard Bedrock across concurrency 1-50, showing throughput can drop over 50% under realistic concurrent load. Doesn't cover Priority/latency-optimized tiers.
- [Respan — Anthropic API vs AWS Bedrock Claude](https://www.respan.ai/articles/claude-vs-bedrock-claude) — anecdotal comparison noting Anthropic's direct API edges out Bedrock on time-to-first-token for US-East traffic.
- [AImultiple — LLM Latency Benchmark](https://aimultiple.com/llm-latency-benchmark) — broader latency/streaming comparison across reasoning and non-reasoning models.

## Bottom line

Within a given tier, most frontier direct APIs land in the same rough 45-170 t/s band for a single request on their latest generation — the differences between OpenAI, Anthropic, Mistral, and Google are smaller than marketing implies, and Anthropic's small/medium/large models in particular have converged to similar speeds. Real 2x+ jumps come from three places: picking a genuinely smaller/different model (Gemini Flash-Lite, GPT-5.6 Luna vs Sol), a speed product with actual independent verification (currently just Anthropic's Fast Mode), or a purpose-built model on different hardware (Codex-Spark) rather than the same model served faster. Provisioned-capacity products (Azure PTUs, Vertex GSUs, Bedrock/Anthropic/Gemini Priority tiers) solve a different, real problem — reliable throughput or reduced overload errors at scale — but most of their per-request speed claims are unverified vendor numbers, and one provider (Gemini) doesn't even claim a speed benefit for its priority tier.
