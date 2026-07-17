# Lumen Voice of Customer Analytics

> Portfolio-grade NLP decision system for turning 50K+ unstructured customer comments into a ranked product backlog.

## Project status

Complete local portfolio build with cached Streamlit artifacts. The heavyweight transformer and BERTopic scripts run offline; the dashboard reads precomputed Parquet/CSV files for free-tier reliability.

## Business problem

Lumen's Product and Support teams cannot consistently answer three questions: what customers complain about, whether those complaints are improving, and which issues deserve scarce engineering capacity in the next two sprints.

## My role

Business Analyst, Data Analyst, and Product Analyst: frame the decision, build and validate the NLP pipeline, translate customer language into product priorities, and communicate the recommendation to the VP of Product.

## Architecture

```mermaid
flowchart LR
    A[Reviews and tickets] --> B[Cleaning and negation handling]
    B --> C[VADER and transformer sentiment]
    B --> D[LDA and BERTopic]
    C --> E[Entity-topic crosswalk]
    D --> E
    E --> F[Impact and RICE prioritization]
    F --> G[Fix simulation and validation]
    F --> H[Cached dashboard datasets]
    G --> H
    H --> I[Streamlit topic explorer]
    H --> J[Executive memo]
```

## Repository map

| Folder | Purpose |
|---|---|
| `01-business-case` | Discovery, decision, constraints, and hypotheses |
| `02-data` | Reproducible synthetic feedback and release calendar |
| `03-preprocessing` | Cleaning, negation scope, and preprocessing EDA |
| `04-sentiment-analysis` | VADER, transformer, disagreement analysis, trends |
| `05-topic-modeling` | LDA, BERTopic, model judgment, topic trends |
| `06-entity-extraction` | SKU and feature extraction and crosswalks |
| `07-product-strategy` | Metrics, prioritization engine, and RICE |
| `08-experiment` | Simulated fix and before/after validation |
| `09-dashboard` | Cloud-safe Streamlit application |
| `10-executive-memo` | VP memo and methodological limitations |

## Tools

Python, pandas, NumPy, Faker, NLTK/VADER, spaCy, gensim, BERTopic, sentence-transformers, Hugging Face Transformers, SciPy, Plotly, and Streamlit.

## Run locally

```powershell
cd lumen-capstone
python -m pip install -r requirements-pipeline.txt
python 02-data/generate_data.py
python 03-preprocessing/text_cleaning.py
python 04-sentiment-analysis/vader_sentiment.py
python 04-sentiment-analysis/sentiment_trend_analysis.py
python 05-topic-modeling/lda_topic_model.py
python 05-topic-modeling/topic_trend_analysis.py
python 06-entity-extraction/ner_feature_extraction.py
python 06-entity-extraction/entity_topic_crosswalk.py
python 07-product-strategy/prioritization_engine.py
python 08-experiment/before_after_simulation.py
```

```powershell
python -m pip install -r 09-dashboard/requirements.txt
streamlit run 09-dashboard/app.py
```

## Validated findings and business impact

- The text-only topic layer recovered the planted `5.4.0` battery signal: battery-topic share rose from **19.3% to 41.1%**, a **113.3% relative increase**.
- The priority engine ranks **performance/crashes**, **battery/charging**, and **setup/account** as the top three issues under the 24 engineer-week constraint.
- Battery/charging has the broadest exposure: **13,106 mentions** and **$1.11M scenario-weighted revenue exposure**.
- The simulated battery remediation reduced 90-day topic volume **63.3%** and improved mean sentiment **0.279 points** (bootstrap 95% CI **0.241–0.318**). This validates the measurement workflow; it is not a causal forecast.

## Recruiter-ready impact bullets

- Built an end-to-end NLP decision system over **50K** multi-source customer comments, combining negation-aware preprocessing, sentiment, topic discovery, entity extraction, and release-aligned trend analysis.
- Independently recovered a planted post-release battery complaint shock—**113% relative growth**—demonstrating pipeline sensitivity to a known product signal.
- Translated unstructured feedback into a capacity-aware backlog using severity, reach, commercial exposure, and RICE, identifying three fixes within a **24 engineer-week** constraint.
- Designed an interactive Streamlit topic explorer with searchable verbatims and cached artifacts, separating offline model compute from free-tier dashboard serving.

## Cloud deployment design

The deployed dashboard will read committed, pre-computed CSV/Parquet artifacts. Transformer inference and topic-model fitting will run offline, avoiding repeated inference on Streamlit Community Cloud's free-tier CPU and memory.

## Methodological note

The generator deliberately includes a post-release complaint spike, typos, sarcasm, mixed sentiment, and multi-issue feedback. These labels are validation scaffolding—not evidence of model performance. The final README will state which patterns the independent analysis actually recovered. A paid LLM could improve aspect extraction and nuanced sentiment, but no paid API is required.
