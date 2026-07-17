# Synthetic data design

## Purpose

The generator creates 50,000 reproducible records across three source-specific schemas over January 2025–June 2026. It uses templates with randomized features, vocabulary, dates, ratings, punctuation, and errors. No paid API is required.

## Deliberately planted patterns

- Release `5.4.0` on June 15, 2025 increases battery complaints sharply and performance complaints moderately through September; later patches produce partial recovery.
- Approximately 14% of all text mixes praise and criticism, such as “I love how this looks fantastic, but the battery dies before lunch.”
- Approximately 4.5% uses overt sarcasm, including “Amazing job, Lumen—now my battery drains while idle.”
- Approximately 24% mentions two or three issues.
- Approximately 11.5% contains a simple deletion/repetition typo; smaller shares include slang, punctuation noise, and hashtags.
- Most support tickets are intentionally untagged; multi-issue tickets take longer to resolve on average.

Exact realized rates are written to `generated/generation_summary.json` each run.

## Validation boundary

`generator_validation_sample.csv` includes planted labels solely for generator QA. Downstream sentiment and topic models must use only the source CSVs and must independently recover patterns from text. This prevents circular validation.

## Run

```powershell
python 02-data/generate_data.py
```

Generation is deterministic with seed 42. Optional count and output-directory arguments support quick tests.

## Known realism limits

Template variation cannot reproduce real language diversity, demographic differences, coordinated review behavior, or subtle sarcasm. Review writers are self-selected and do not represent the full customer population.

## So what?

The planted release shock supplies a known-answer test: if the independent pipeline cannot find it, its results should not drive a roadmap decision.
