"""Generate reproducible, messy synthetic Voice-of-Customer data for Lumen.

Outputs preserve the requested source schemas. A separate audit sample contains
generator-only labels for QA; downstream models must never train on those labels.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)
SPIKE_DATE = date(2025, 6, 15)
OUTPUT_DIR = Path(__file__).resolve().parent / "generated"

SKUS = ["LUMEN-BUDS-2", "LUMEN-WATCH-X", "LUMEN-HUB-MINI"]
FEATURES = {
    "battery": ["battery", "charge", "charging", "battery life", "power drain"],
    "performance": ["app", "performance", "interface", "firmware", "screen"],
    "connectivity": ["bluetooth", "pairing", "connection", "wifi", "sync"],
    "audio": ["sound", "microphone", "audio", "volume", "noise cancellation"],
    "design": ["design", "fit", "screen", "buttons", "case"],
    "setup": ["setup", "login", "installation", "onboarding", "account"],
    "delivery": ["delivery", "box", "shipping", "package", "replacement"],
}

NEGATIVE = {
    "battery": ["dies before lunch", "barely lasts {hours} hours", "drains while idle", "won't hold a charge", "needs charging twice a day"],
    "performance": ["freezes every few minutes", "became painfully slow", "keeps crashing", "lags after every tap", "stutters constantly"],
    "connectivity": ["disconnects at random", "refuses to pair", "drops the connection", "won't sync", "forgets my device"],
    "audio": ["microphone sounds muffled", "audio cuts out", "volume is too low", "noise cancellation got worse", "sound crackles"],
    "design": ["hurts after an hour", "buttons feel cheap", "case scratches easily", "screen is hard to read", "fit is uncomfortable"],
    "setup": ["setup loops forever", "login never completes", "instructions are confusing", "account linking fails", "onboarding is broken"],
    "delivery": ["arrived late", "box was damaged", "replacement never came", "wrong item was shipped", "package was already open"],
}

POSITIVE = [
    "looks fantastic", "works exactly as promised", "feels premium", "was easy to set up",
    "has excellent sound", "is surprisingly responsive", "fits perfectly", "made my routine easier",
]
INTROS = ["Honestly", "After the latest update", "For the price", "Three weeks in", "Since yesterday", "Quick update", "Not gonna lie", "Sadly"]
ENDINGS = ["Please fix this.", "Support, can you help?", "Expected better from Lumen.", "Would not recommend right now.", "Hope the next patch sorts it out.", "This is getting old."]
SARCASM = [
    "Amazing job, Lumen—now my {feature} {problem}.",
    "Love paying premium prices so the {feature} {problem}.",
    "Exactly what I wanted: a device that {problem}.",
    "Five stars for making sure the {feature} {problem}. Just kidding.",
]


@dataclass(frozen=True)
class TextRecord:
    text: str
    issues: tuple[str, ...]
    is_mixed: bool
    is_sarcastic: bool
    has_typo: bool
    is_positive: bool


def random_date(rng: np.random.Generator) -> date:
    span = (END_DATE - START_DATE).days
    return START_DATE + timedelta(days=int(rng.integers(0, span + 1)))


def issue_weights(on_date: date, source: str) -> np.ndarray:
    """Return date-aware topic probabilities; 5.4.0 plants a recoverable spike."""
    names = list(FEATURES)
    weights = dict(zip(names, [0.16, 0.13, 0.18, 0.14, 0.13, 0.14, 0.12]))
    if SPIKE_DATE <= on_date < date(2025, 10, 1):
        weights["battery"] *= 3.3
        weights["performance"] *= 2.15
    elif date(2025, 10, 1) <= on_date < date(2026, 2, 1):
        weights["battery"] *= 2.0
        weights["performance"] *= 1.45
    if source == "app_store_reviews":
        weights["performance"] *= 1.4
        weights["setup"] *= 1.25
        weights["delivery"] *= 0.15
    elif source == "support_tickets":
        weights["setup"] *= 1.35
        weights["delivery"] *= 1.2
    values = np.array([weights[name] for name in names], dtype=float)
    return values / values.sum()


def add_typo(text: str, rng: random.Random) -> str:
    words = text.split()
    candidates = [i for i, word in enumerate(words) if len(re.sub(r"\W", "", word)) >= 5]
    if not candidates:
        return text
    idx = rng.choice(candidates)
    word = words[idx]
    pos = rng.randrange(1, len(word) - 1)
    if rng.random() < 0.5:
        word = word[:pos] + word[pos + 1 :]
    else:
        word = word[:pos] + word[pos] + word[pos:]
    words[idx] = word
    return " ".join(words)


def make_text(on_date: date, source: str, rng: random.Random, np_rng: np.random.Generator) -> TextRecord:
    topics = list(FEATURES)
    issue_count = int(np_rng.choice([1, 2, 3], p=[0.72, 0.23, 0.05]))
    issues = tuple(np_rng.choice(topics, size=issue_count, replace=False, p=issue_weights(on_date, source)).tolist())
    mixed = rng.random() < 0.17
    sarcastic = rng.random() < 0.055
    positive_rate = {"product_reviews": 0.26, "support_tickets": 0.035, "app_store_reviews": 0.20}[source]
    is_positive = rng.random() < positive_rate
    if is_positive:
        issues = (issues[0],)
    primary = issues[0]
    feature = rng.choice(FEATURES[primary])
    problem = rng.choice(NEGATIVE[primary]).format(hours=rng.choice([2, 3, 4, 5, 6]))

    if is_positive:
        sarcastic = False
        mixed = False
        text = f"{rng.choice(INTROS)}, the {feature} {rng.choice(POSITIVE)}."
    elif sarcastic:
        text = rng.choice(SARCASM).format(feature=feature, problem=problem)
    elif mixed:
        text = f"I love how this {rng.choice(POSITIVE)}, but the {feature} {problem}."
    else:
        text = f"{rng.choice(INTROS)}, the {feature} {problem}."

    if not is_positive:
        for issue in issues[1:]:
            other_feature = rng.choice(FEATURES[issue])
            other_problem = rng.choice(NEGATIVE[issue]).format(hours=rng.choice([2, 3, 4, 5, 6]))
            text += f" Also, the {other_feature} {other_problem}."

    if rng.random() < 0.64:
        text += " " + rng.choice(ENDINGS)
    if rng.random() < 0.12:
        text = text.replace(".", rng.choice(["!!", "...", "."]), 1)
    if rng.random() < 0.07:
        text += " " + rng.choice(["ugh", "smh", ":/", "???", "#notimpressed"])
    has_typo = rng.random() < 0.115
    if has_typo:
        text = add_typo(text, rng)
    return TextRecord(text, issues, mixed, sarcastic, has_typo, is_positive)


def star_rating(record: TextRecord, rng: np.random.Generator) -> int:
    base = (4.45 if record.is_positive else 2.0) + (0.65 if record.is_mixed else 0) - 0.28 * (len(record.issues) - 1)
    return int(np.clip(round(rng.normal(base, 0.9)), 1, 5))


def generate_source(source: str, count: int, faker: Faker, rng: random.Random, np_rng: np.random.Generator) -> tuple[pd.DataFrame, list[dict]]:
    rows: list[dict] = []
    audit: list[dict] = []
    for i in range(count):
        on_date = random_date(np_rng)
        rec = make_text(on_date, source, rng, np_rng)
        sku = str(np_rng.choice(SKUS, p=[0.43, 0.32, 0.25]))
        rating = star_rating(rec, np_rng)
        common_audit = {
            "source": source, "date": on_date.isoformat(), "text": rec.text,
            "planted_issues": "|".join(rec.issues), "is_mixed": rec.is_mixed,
            "is_sarcastic": rec.is_sarcastic, "has_typo": rec.has_typo,
            "is_positive": rec.is_positive,
        }
        if source == "product_reviews":
            record_id = f"PR-{i + 1:06d}"
            rows.append({"review_id": record_id, "product_sku": sku, "star_rating": rating, "review_text": rec.text, "review_date": on_date.isoformat(), "verified_purchase": rng.random() < 0.84})
        elif source == "support_tickets":
            record_id = f"ST-{i + 1:06d}"
            tag = rec.issues[0] if rng.random() < 0.16 else None
            resolution = max(0.4, float(np_rng.lognormal(2.15 + 0.24 * (len(rec.issues) - 1), 0.65)))
            rows.append({"ticket_id": record_id, "customer_id": faker.bothify("CUST-######"), "ticket_text": rec.text, "category_tag": tag, "resolution_time_hours": round(resolution, 2), "created_date": on_date.isoformat()})
        else:
            record_id = f"AR-{i + 1:06d}"
            platform = str(np_rng.choice(["ios", "android"], p=[0.46, 0.54]))
            if on_date < SPIKE_DATE:
                version = "5.3.2"
            elif on_date < date(2025, 10, 1):
                version = "5.4.0"
            elif on_date < date(2026, 2, 1):
                version = "5.4.2"
            else:
                version = "5.5.0"
            rows.append({"review_id": record_id, "platform": platform, "star_rating": rating, "review_text": rec.text, "app_version": version, "review_date": on_date.isoformat()})
        common_audit["record_id"] = record_id
        audit.append(common_audit)
    return pd.DataFrame(rows), audit


def rate(rows: Iterable[dict], key: str) -> float:
    rows = list(rows)
    return round(sum(bool(row[key]) for row in rows) / len(rows), 4)


def build_summary(frames: dict[str, pd.DataFrame], audit: list[dict]) -> dict:
    before = [r for r in audit if r["date"] < SPIKE_DATE.isoformat()]
    spike = [r for r in audit if SPIKE_DATE.isoformat() <= r["date"] < "2025-10-01"]
    before_complaints = [r for r in before if not r["is_positive"]]
    spike_complaints = [r for r in spike if not r["is_positive"]]
    battery_before = sum("battery" in r["planted_issues"].split("|") for r in before_complaints) / len(before_complaints)
    battery_spike = sum("battery" in r["planted_issues"].split("|") for r in spike_complaints) / len(spike_complaints)
    issue_counts = Counter(issue for row in audit for issue in row["planted_issues"].split("|"))
    return {
        "seed": SEED,
        "date_range": [START_DATE.isoformat(), END_DATE.isoformat()],
        "records": {name: len(df) for name, df in frames.items()},
        "total_records": sum(len(df) for df in frames.values()),
        "messiness_rates": {"positive_only": rate(audit, "is_positive"), "mixed_sentiment": rate(audit, "is_mixed"), "sarcasm": rate(audit, "is_sarcastic"), "typos": rate(audit, "has_typo"), "multi_issue": round(sum("|" in r["planted_issues"] for r in audit) / len(audit), 4)},
        "issue_mentions": dict(issue_counts.most_common()),
        "planted_signal": {
            "release_date": SPIKE_DATE.isoformat(),
            "pre_release_battery_share": round(battery_before, 4),
            "spike_window_battery_share": round(battery_spike, 4),
            "relative_lift": round(battery_spike / battery_before - 1, 4),
            "note": "Generator-label audit only; downstream recovery must use text-derived topics.",
        },
        "support_untagged_rate": round(frames["support_tickets"]["category_tag"].isna().mean(), 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-reviews", type=int, default=20_000)
    parser.add_argument("--support-tickets", type=int, default=18_000)
    parser.add_argument("--app-reviews", type=int, default=12_000)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    faker = Faker("en_US")
    Faker.seed(SEED)
    rng = random.Random(SEED)
    np_rng = np.random.default_rng(SEED)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    specs = {"product_reviews": args.product_reviews, "support_tickets": args.support_tickets, "app_store_reviews": args.app_reviews}
    frames: dict[str, pd.DataFrame] = {}
    audit: list[dict] = []
    for source, count in specs.items():
        frames[source], source_audit = generate_source(source, count, faker, rng, np_rng)
        frames[source].to_csv(args.output_dir / f"{source}.csv", index=False)
        audit.extend(source_audit)

    summary = build_summary(frames, audit)
    (args.output_dir / "generation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    audit_df = pd.DataFrame(audit)
    sampled = pd.concat(
        [group.sample(min(25, len(group)), random_state=SEED) for _, group in audit_df.groupby(["is_mixed", "is_sarcastic"], dropna=False)],
        ignore_index=True,
    )
    sampled.to_csv(args.output_dir / "generator_validation_sample.csv", index=False)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
