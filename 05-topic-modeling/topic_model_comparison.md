# LDA vs. BERTopic

LDA is inexpensive, transparent, and useful as a baseline, but Lumen's short, colloquial, multi-issue comments violate its bag-of-words assumptions. Closely related concepts can split across topics, while generic complaint words dominate multiple clusters.

BERTopic is the more useful production candidate for this business use case because sentence embeddings retain semantic similarity across different wording and produce clusters that are easier for Product Managers to inspect as customer problems. Its disadvantages are higher compute/memory, sensitivity to embedding and density parameters, and occasional outlier-heavy clusters.

**Judgment:** use BERTopic offline for topic discovery, then map stable human-approved labels into a lightweight production classifier. Retain LDA as a reproducible benchmark and stability check. Neither model should assign roadmap priority without verbatim review and human label validation.

## So what?

Lumen should pay the offline compute cost for better topic discovery, but deploy only cached assignments and governed labels—not a fragile clustering job inside the dashboard.

