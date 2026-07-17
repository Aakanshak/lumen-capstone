"""Business-facing topic assignment and planted-signal validation."""
from pathlib import Path
import json, re, pandas as pd
PATTERNS={"Battery & charging":r"battery|charge|charging|power drain","Performance & crashes":r"freeze|slow|crash|lag|stutter|performance|firmware","Connectivity & sync":r"bluetooth|pair|connection|wifi|sync|disconnect","Audio quality":r"sound|microphone|audio|volume|noise cancellation|crackle","Design & comfort":r"design|fit|screen|button|case|uncomfortable","Setup & account":r"setup|login|installation|onboarding|account","Delivery & replacement":r"delivery|box|shipping|package|replacement|arrived"}
def topics(text):
 found=[name for name,p in PATTERNS.items() if re.search(p,text,re.I)]; return found or ["Other"]
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"04-sentiment-analysis"/"outputs"/"vader_scored.parquet"); df["topic_list"]=df.text.map(topics); ex=df.explode("topic_list").rename(columns={"topic_list":"topic"}); ex["month"]=pd.to_datetime(ex.date).dt.to_period("M").dt.to_timestamp(); ex["severity"]=(-ex.vader_compound).clip(lower=0)
 target=root/"05-topic-modeling"/"outputs"; target.mkdir(exist_ok=True); ex.to_parquet(target/"feedback_topics.parquet",index=False)
 trends=ex.groupby(["month","topic","source"]).agg(volume=("record_id","size"),mean_sentiment=("vader_compound","mean"),severity=("severity","mean")).reset_index(); trends.to_csv(target/"topic_trends.csv",index=False)
 battery=ex[ex.topic=="Battery & charging"]; pre=(battery.date<pd.Timestamp("2025-06-15")).sum()/(df.date<pd.Timestamp("2025-06-15")).sum(); spike=((battery.date>=pd.Timestamp("2025-06-15"))&(battery.date<pd.Timestamp("2025-10-01"))).sum()/((df.date>=pd.Timestamp("2025-06-15"))&(df.date<pd.Timestamp("2025-10-01"))).sum(); result={"pre_share":round(pre,4),"spike_share":round(spike,4),"relative_lift":round(spike/pre-1,4),"recovered":bool(spike/pre>=1.5)}; (target/"planted_signal_validation.json").write_text(json.dumps(result,indent=2))
 print(result,"So what? The text-only topic layer independently tests whether the known release shock is recoverable.")
if __name__=="__main__": main()

