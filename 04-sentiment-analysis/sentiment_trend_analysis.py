from pathlib import Path
import pandas as pd
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"04-sentiment-analysis"/"outputs"/"vader_scored.parquet"); df["month"]=pd.to_datetime(df.date).dt.to_period("M").dt.to_timestamp()
 out=df.groupby(["month","source","product_sku"],dropna=False).agg(feedback_volume=("record_id","size"),mean_sentiment=("vader_compound","mean"),negative_share=("vader_sentiment",lambda s:(s=="negative").mean())).reset_index(); out.to_csv(root/"04-sentiment-analysis"/"outputs"/"sentiment_trends.csv",index=False)
 print("So what? Release-aligned trend breaks identify when Product should investigate causality rather than treating aggregate sentiment as static.")
if __name__=="__main__": main()

