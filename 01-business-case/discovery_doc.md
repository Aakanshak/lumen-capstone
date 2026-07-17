# Discovery document

## Executive context

Lumen is a fictional consumer electronics and companion-app company. Customer feedback arrives through product reviews, support tickets, and iOS/Android reviews, but most of the text is never systematically read.

## Current-state indicators (simulated baseline)

- NPS declined from approximately 42 to 31 over the last two quarters.
- CSAT declined from approximately 4.3/5 to 3.8/5 after the June 15, 2025 firmware/app release.
- More than 50,000 comments accumulated over 18 months; roughly 85% of tickets are untagged.
- Product managers rely on anecdotes and escalations; Support manually triages text and applies inconsistent categories.

These values are business-case assumptions, not measured findings. The pipeline must calculate and validate analytical results from generated data.

## Stakeholder pain

| Stakeholder | Pain | Decision need |
|---|---|---|
| VP Product | No comparable measure of issue size and severity | Which issues enter the next two sprints? |
| Product Managers | Roadmap debate is driven by loud anecdotes | Which product, feature, and release owns each issue? |
| Support Operations | Manual triage is slow and inconsistent | Which contacts can be routed or proactively deflected? |
| Engineering | Requests arrive without impact estimates | What is the expected customer and commercial value? |

## Problem statement

Lumen lacks a repeatable way to convert unstructured feedback into reliable, release-aware product priorities. The project will identify complaint topics, quantify severity and trends, connect issues to products/features, and rank fixes while explicitly communicating NLP uncertainty and sampling bias.

## Success criteria

1. Recover the planted post-release battery/performance shift without using generator labels as model inputs.
2. Produce interpretable topic and sentiment evidence with verbatim examples.
3. Rank an actionable backlog under a two-sprint capacity constraint.
4. Provide cached artifacts that make the dashboard responsive and cloud deployable.

## So what?

This converts an unread-feedback problem into a decision system: leaders can see what changed, inspect the customer language behind it, and choose fixes with a transparent evidence trail.

