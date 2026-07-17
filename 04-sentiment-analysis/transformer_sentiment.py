"""Offline CPU transformer inference, saved once for dashboard consumption."""
from pathlib import Path
import argparse, pandas as pd

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--model",default="distilbert-base-uncased-finetuned-sst-2-english"); parser.add_argument("--batch-size",type=int,default=64); args=parser.parse_args()
    from transformers import pipeline
    root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"04-sentiment-analysis"/"outputs"/"vader_scored.parquet")
    clf=pipeline("sentiment-analysis",model=args.model,device=-1)
    predictions=[]
    for start in range(0,len(df),args.batch_size): predictions.extend(clf(df.text.iloc[start:start+args.batch_size].tolist(),truncation=True,max_length=256,batch_size=args.batch_size))
    df["transformer_label"]=[p["label"].lower() for p in predictions]; df["transformer_confidence"]=[p["score"] for p in predictions]
    df.to_parquet(root/"04-sentiment-analysis"/"outputs"/"transformer_scored.parquet",index=False)
    print("So what? A contextual model improves phrasing sensitivity, but a document label still collapses aspect-level mixed sentiment and can miss sarcasm.")
if __name__=="__main__": main()

