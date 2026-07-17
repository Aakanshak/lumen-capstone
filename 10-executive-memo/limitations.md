# Limitations and bias

- **Review sample bias:** people who leave reviews or contact Support are self-selected and are not representative of all customers. Counts should eventually be normalized by active users, sales, version exposure, and product tenure.
- **Synthetic-language bias:** templates cannot reproduce real demographic, cultural, multilingual, adversarial, or emerging language patterns.
- **Sarcasm:** both lexicon and general transformer models can fail when literal positive wording implies a negative intent.
- **Mixed/aspect sentiment:** one document-level score loses the distinction between “love the design” and “battery is terrible.” Negation scoping helps but does not solve aspect attribution.
- **Topic instability:** LDA and BERTopic assignments vary with preprocessing, hyperparameters, random seed, embedding model, and time. Labels require human-in-the-loop validation.
- **Causal inference:** release alignment and before/after differences do not prove the release caused the change. A real evaluation needs exposure data and a credible comparison group or phased rollout.
- **Commercial estimates:** revenue/churn weights are scenarios, not audited forecasts.

With more time and real data, I would add multilingual handling, aspect-based sentiment, a labeled human-review set, temporal topic-stability tests, custom classifier fine-tuning, customer exposure denominators, and a controlled rollout measurement design.

## So what?

These outputs prioritize investigation; they do not replace representative customer research, engineering diagnosis, or causal measurement.

