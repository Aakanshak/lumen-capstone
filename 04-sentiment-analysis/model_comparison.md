# VADER vs. transformer sentiment

The dashboard disagreement panel uses a transparent context-aware proxy until the optional CPU transformer job is run and cached. The production script uses DistilBERT and never runs in Streamlit.

Typical disagreements include sarcastic praise (“Five stars … just kidding”), mixed aspect statements (“love the design, but the battery dies”), and negated positives (“not good”). VADER benefits from punctuation and explicit polarity words but often reads sarcastic praise literally. A transformer uses context, yet a general SST-2 model still compresses multiple aspect opinions into one document label and is not guaranteed to recognize product-domain sarcasm.

## So what?

Agreement is a monitoring signal, not accuracy. High-impact disagreements should be sampled for human review and eventually used to fine-tune an aspect-based classifier.

