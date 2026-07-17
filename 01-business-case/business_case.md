# Business case

## Decision at stake

Select at most three customer-facing issues for the next two two-week sprints. The recommendation must balance reach, complaint severity, confidence, commercial/churn exposure, and engineering effort.

## Assumptions

- Product portfolio: `LUMEN-BUDS-2`, `LUMEN-WATCH-X`, `LUMEN-HUB-MINI`, and the shared Lumen mobile app.
- Analysis window: January 1, 2025 through June 30, 2026.
- Trigger release: firmware/app `5.4.0`, released June 15, 2025.
- Capacity: 24 engineer-weeks across two sprints; no more than three major fixes.
- Revenue/churn weights are scenario estimates for prioritization, not finance forecasts.
- Human review remains required for high-impact classifications.

## Hypotheses

1. Battery and performance complaints rise materially after release `5.4.0`, especially for `LUMEN-BUDS-2` and Android.
2. Star ratings and sentiment scores deteriorate after the release, with partial recovery after later patches.
3. Support-ticket resolution time is higher for multi-issue comments and untagged tickets.
4. VADER and the transformer disagree disproportionately on sarcasm, negation, and mixed-sentiment text.
5. Embedding-based topics are more actionable than LDA for short, colloquial feedback, while LDA remains cheaper and easier to explain.

## Constraints and risks

- Synthetic text cannot reproduce every linguistic or behavioral feature of real customers.
- Review writers are self-selected and are not representative of all customers.
- Topic labels are unstable across models and hyperparameters.
- Mixed sentiment can contain positive and negative opinions about different aspects; a single document score loses that structure.
- Negation scope is handled heuristically and is not fully solved.

## Decision rule

Use a weighted issue score combining normalized volume, negative-sentiment intensity, trend acceleration, entity exposure, and estimated commercial impact. Cross-check the leading issues with RICE and verbatim review before recommending shipment.

## So what?

The business case defines a constrained roadmap choice—not merely an NLP exercise—so model outputs must end in a defensible, capacity-aware product recommendation.

