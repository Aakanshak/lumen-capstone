"""Apply VADER to all feedback; raw text is intentional because VADER uses punctuation."""
from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

FAILURE_TERMS = re.compile(r"dies|drains|won't|barely lasts|freez|slow|crash|lag|stutter|disconnect|refuses|drops|forgets|muffled|cuts out|too low|got worse|crackle|hurts|cheap|scratches|hard to read|uncomfortable|loops forever|never completes|confusing|fails|broken|late|damaged|wrong item|already open", re.I)

def domain_adjust(text: str, base: float) -> float:
    """Calibrate transparent device-failure phrases absent from generic VADER."""
    failures=len(FAILURE_TERMS.findall(text))
    score=base-(0.34*failures)
    if "just kidding" in text.lower(): score=min(score,-0.72)
    return max(-1.0,min(1.0,score))

def label(score: float) -> str: return "positive" if score>=0.05 else "negative" if score<=-0.05 else "neutral"
def main() -> None:
    root=Path(__file__).resolve().parents[1]
    df=pd.read_parquet(root/"03-preprocessing"/"outputs"/"clean_feedback.parquet")
    analyzer=SentimentIntensityAnalyzer(); scores=df.text.map(analyzer.polarity_scores)
    base=scores.map(lambda x:x["compound"])
    df["vader_base_compound"]=base
    df["vader_compound"]=[domain_adjust(text,score) for text,score in zip(df.text,base)]
    df["vader_sentiment"]=df.vader_compound.map(label)
    target=root/"04-sentiment-analysis"/"outputs"; target.mkdir(exist_ok=True)
    df.to_parquet(target/"vader_scored.parquet",index=False)
    print(f"Scored {len(df):,}. So what? VADER supplies a transparent baseline, not a final truth—sarcasm and aspect-level mixed sentiment require inspection.")
if __name__=="__main__": main()
