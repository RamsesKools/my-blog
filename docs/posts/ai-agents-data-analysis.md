---
date: 2026-07-30
slug: ai-agents-data-analysis
tags:
  - AI
  - Workflow
  - Data
---

# Automating data analysis with AI coding agents

Asking an AI agent to "check whether these two tables match" gets you an answer in about ninety seconds.
The answer is confident, well formatted, and there is a decent chance it is wrong.

The problem isn't that the agent can't write SQL; it can.
The problem is that a question about data can be interpreted in a large number of ways, and the agent has no way to know how to answer unless you tell it.
So I stopped asking better questions and started building the workspace the question gets asked in.

<!-- more -->

I spent a few sprints validating a data platform migration: the same tables produced by an old pipeline and a new one, and a decision to make about whether consumers could switch.
Dozens of tables, the same method each time, high enough stakes that a wrong "looks fine" would land in production.
That is exactly the shape of work an agent should be good at, and exactly the shape it fails at by default.

Here is what actually made it work.

## What doesn't work: just asking

The first attempt was the obvious one.
Point the agent at the cluster, describe the two tables, ask whether they match.

It wrote a query joining both sides on the id column, per day, counted the mismatches, and reported 8% data loss.

Every part of that was wrong, and none of it looked wrong:

- The id column was not the business key. It was only unique within a partner, so the join fanned out.
- The two pipelines partition on different clocks, so a record that shifted across midnight was counted as both missing on one day and extra on the next. The same healthy record, reported twice as a fault.
- The new table's history had two eras. Older rows were bulk-migrated and completely empty, newer rows were produced natively and fine. Averaged together, that reads as uniform corruption.

The agent did nothing unreasonable.
It just didn't know any of that, and nothing in the environment was going to tell it.

## The fix is three files, not a better prompt

What changed things was treating the agent's environment as the deliverable.
Three pieces, in increasing order of how much they helped.

### 1. A workspace it can actually run

A small `uv` project: two modules, a `sql/` folder, a `notebooks/` folder.
The modules wrap the [Redshift Data API](https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html) and a direct connector so that every query, either route, returns a pandas DataFrame.

That sounds trivial. It removes an entire category of failure.
When `run_sql` is one import away and always returns a DataFrame, the agent spends its effort on the question instead of reinventing connection handling in every notebook, slightly differently, with a new bug each time.

The other thing the workspace buys you is target safety.
Config is read from target-prefixed variables, `REDSHIFT_DATA_API_ACC_*` and `REDSHIFT_DATA_API_PRD_*`, and every call takes an explicit `target="ACC"`.
A kernel you have had open all afternoon cannot silently start answering from production.

### 2. A skill file: the operating manual

This is the one that mattered most, and it is just a markdown file.

[Skills](https://code.claude.com/docs/en/skills) are instructions an agent loads when a task matches.
Mine covers the things that are true about this environment and nowhere else:

- Which notebook editing tools to use, and that it must never touch raw `.ipynb` JSON.
- The setup-cell pattern: every schema, table, window and column list is a constant in one cell.
- That the SSO token will expire mid-analysis, that `aws login` needs a human at a browser, and that the agent should stop and ask rather than burn twenty minutes retrying.
- A table of Redshift-specific SQL traps. `count(distinct a, b)` isn't valid. `rows` is reserved. `<>` silently drops NULL-vs-value pairs, so use `is distinct from`. Each of those costs an afternoon exactly once, and then never again.

None of this is clever. It is the stuff a new colleague learns in their first two weeks, written down.
The difference is that the agent starts every session as a new colleague.

### 3. A prompt file: the method

The skill says how to work here.
The prompt file says what to do, in order, for one recurring job.

Mine is about twenty lines and its most valuable feature is that it tells the agent when to stop:

> Confirm the parameters with me before running the gates: business key, message key, child arrays, consumers, consumed columns. **Measure the business key**, do not take it from the documentation, it has been wrong before.
>
> Stop and check with me if a gate fails, if a result contradicts what you read in step 2, or if a query is about to run against anything other than the scratch tables.

An agent that runs the whole method unsupervised produces a report nobody trusts.
An agent that stops at three checkpoints produces one that survives review.

## The habit that makes the output trustworthy

If you take one thing from this: **make the agent write its findings as markdown cells, in the notebook, directly under the output that supports them, with the actual numbers pasted in.**

Not a summary in the chat window. Not a separate report written afterwards from memory.
A markdown cell, next to the query result, saying what that specific number means.

This does three things at once.
It forces the claim to sit next to its evidence, where a reviewer can check it in one glance.
It survives the chat session, which is where analysis normally goes to die.
And it is genuinely the thing agents are best at, because they can read the output they just produced and describe it accurately.

The notebook stops being a scratchpad and becomes the deliverable.

Two supporting habits make that hold up:

**Parameterise at the top.** Every table name, date window and column list lives in the setup cell.
The notebook is then a function of that cell, it can be re-pointed at the next table in one edit, and it re-runs top to bottom after a kernel restart.

**Assume the kernel will restart.** It will, because the SSO token expires and boto3 caches its session, so a restart is the only fix.
Any cell that depends on a variable which only exists because some exploratory cell happened to run once is a cell you will lose.
Expensive intermediates belong in scratch tables, not in kernel memory.

## Traps an agent walks into cheerfully

Worth writing into your own skill file, because they generalise past my specific migration:

**Check whether the history is uniform before comparing anything.**
A backfilled table is often two datasets wearing one name.
Find the boundary first, then run your comparisons on one era at a time.

**Compare at set level, not per day.**
If two systems partition on different clocks, a day-by-day join reports every boundary-crossing record as two separate faults.
Take keys from one side's window and search the *entire* opposite table.

**Run it in both directions.**
Missing records and extra records have completely different causes and completely different fixes.
In my case the "extra" records turned out to be rows the *old* pipeline had dropped, which flipped the conclusion from a concern into a point in the new pipeline's favour.

**A concentrated difference is a boundary artefact. A spread one is a broken pipeline.**
Same percentage, opposite meaning. Always look at the distribution, never just the total.

**No dual-axis charts.**
Two measures on different scales get two panels sharing an x-axis.
A second y-axis lets you slide the crossover point anywhere you like, which means the chart shows whatever you want it to show.
Agents produce dual-axis charts constantly, because most plotting tutorials do.

## What it actually buys you

Not speed, exactly. The first table took longer than doing it by hand.

What it buys is that table twelve is done the same way as table one, that the reasoning is written down next to the numbers, and that when someone asks "how did you decide this" in four months there is a notebook that answers.

The agent is good at the mechanical parts: writing the query, casting the columns, formatting the chart, describing the output in prose.
It is bad at knowing which of those outputs is meaningless.
That judgement stays with you, and the three files above are how you hand over the first part without giving away the second.

## The starter repo

I put a minimal version of the setup on GitHub: [redshift-agent-workspace](https://github.com/RamsesKools/redshift-agent-workspace).

Two modules, two example notebooks, a skill file and a prompt file.
The getting-started notebook walks through connecting, running inline SQL, running SQL from a file, pushing the result into pandas, charting it, and writing the finding down.
The second notebook is a full table comparison with the gates in the order they have to run.

It is a template, not a framework. Clone it, point it at a question, throw the notebooks away when you are done.
