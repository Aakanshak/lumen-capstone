"""Text preprocessing with explicit, inspectable negation scoping."""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

NEGATORS = {"not", "no", "never", "neither", "nor", "hardly", "isn't", "wasn't", "don't", "doesn't", "didn't", "won't", "can't", "cannot"}
STOPWORDS = {"a","an","the","and","or","to","of","for","in","on","with","this","that","it","my","is","was","are","be","after","every","how"}

def normalize_contractions(text: str) -> str:
    replacements = {"can't":"can not", "won't":"will not", "isn't":"is not", "wasn't":"was not", "don't":"do not", "doesn't":"does not", "didn't":"did not"}
    out = text.lower()
    for old, new in replacements.items(): out = out.replace(old, new)
    return out

def tokenize_with_negation(text: str, scope: int = 3) -> list[str]:
    """Append _NEG to up to `scope` content tokens after a negator.

    Scope ends at punctuation or contrast conjunctions. This preserves the
    distinction between `good` and `not good`, but remains a documented heuristic.
    """
    text = normalize_contractions(text)
    raw = re.findall(r"[a-z]+(?:'[a-z]+)?|[.!?,;:]", text)
    result, remaining = [], 0
    for token in raw:
        if token in ".!?,;:" or token in {"but", "however", "although", "yet"}:
            remaining = 0
            continue
        if token in NEGATORS or token == "not":
            result.append("not")
            remaining = scope
            continue
        if token not in STOPWORDS:
            result.append(f"{token}_NEG" if remaining else token)
        if remaining: remaining -= 1
    return result

def clean_text(text: str) -> str:
    return " ".join(tokenize_with_negation(str(text)))

def load_unified(data_dir: Path) -> pd.DataFrame:
    specs = [
        ("product_reviews", "review_id", "review_text", "review_date"),
        ("support_tickets", "ticket_id", "ticket_text", "created_date"),
        ("app_store_reviews", "review_id", "review_text", "review_date"),
    ]
    frames=[]
    for source, id_col, text_col, date_col in specs:
        df=pd.read_csv(data_dir/f"{source}.csv")
        df["source"],df["record_id"],df["text"],df["date"]=source,df[id_col],df[text_col],pd.to_datetime(df[date_col])
        if "product_sku" not in df: df["product_sku"]="LUMEN-APP" if source=="app_store_reviews" else "UNSPECIFIED"
        if "star_rating" not in df: df["star_rating"]=pd.NA
        frames.append(df[["record_id","source","date","product_sku","star_rating","text"]])
    out=pd.concat(frames,ignore_index=True)
    out["clean_text"]=out.text.map(clean_text)
    return out

def main() -> None:
    root=Path(__file__).resolve().parents[1]
    out=load_unified(root/"02-data"/"generated")
    target=root/"03-preprocessing"/"outputs"; target.mkdir(exist_ok=True)
    out.to_parquet(target/"clean_feedback.parquet",index=False)
    examples=out.assign(raw_length=out.text.str.split().str.len(),clean_length=out.clean_text.str.split().str.len()).sample(30,random_state=42)
    examples.to_csv(target/"before_after_examples.csv",index=False)
    print(f"Wrote {len(out):,} cleaned records. So what? Negation-aware tokens reduce avoidable polarity reversals while preserving raw verbatims for human review.")
if __name__=="__main__": main()

