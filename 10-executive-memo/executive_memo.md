# Executive memo: what Lumen should fix next

**To:** VP of Product  
**Decision:** Allocate the next two sprints to performance stability, battery/charging, and setup/account reliability, subject to engineering sizing and verbatim review.

## Why this matters

Lumen has 50,000 comments across product reviews, support tickets, and app stores, while 84.5% of simulated support tickets are untagged. Manual triage cannot consistently connect customer language to releases or product ownership.

## What the analysis found

The text-only pipeline recovered the deliberately hidden release signal without using generator labels. Battery-topic share increased from 19.3% before release `5.4.0` to 41.1% during the following spike window—a 113.3% relative increase. This validates that the method can detect the known pattern embedded in the corpus.

The weighted backlog ranks performance/crashes first (priority score 54.1), battery/charging second (48.8), and setup/account third (47.7). Performance has the greatest negative intensity; battery has the widest exposure, with 13,106 mentions and approximately $1.11M in scenario-weighted revenue exposure. These dollar values are prioritization assumptions, not finance forecasts.

Model disagreement remains material in sarcasm, negation, and mixed-aspect feedback. For that reason, the dashboard makes customer verbatims—not only aggregate scores—the centerpiece of each topic decision.

## Recommendation

1. **Stabilize crashes and lag:** instrument crash-free sessions by version and fix the highest-frequency failure path.
2. **Reduce background battery drain:** audit the `5.4.0` sync redesign and ship a monitored remediation.
3. **Repair setup/account flows:** target login loops and account-link failures while monitoring Support resolution time.

These three issues consume an assumed 23 engineer-weeks, fitting the 24 engineer-week capacity constraint. Confirm sizing before sprint commitment and retain one week as contingency.

## Expected impact and validation

The battery-fix simulation reduced 90-day complaint volume by 63.3% and improved mean sentiment by 0.279 points (bootstrap 95% CI: 0.241–0.318). This demonstrates the measurement workflow, not expected causal lift. A real release should use version exposure denominators, a staged rollout or comparable cohort, and predeclared guardrails.

## Limitations

Review writers are self-selected and do not represent all customers. Synthetic templates understate real linguistic diversity. Sentiment models struggle with sarcasm and mixed aspects; topic models are sensitive to preprocessing and hyperparameters. Release alignment is not causality, and commercial weights are scenarios. Human validation and representative research remain required.

## So what?

Lumen now has a transparent route from customer language to a capacity-aware backlog, with inspectable evidence and explicit uncertainty rather than anecdote-driven prioritization.

