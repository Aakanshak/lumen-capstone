from pathlib import Path
import pandas as pd
IMPACT={"Battery & charging":1.00,"Performance & crashes":.90,"Connectivity & sync":.82,"Audio quality":.70,"Setup & account":.62,"Design & comfort":.55,"Delivery & replacement":.48,"Other":.25}
EFFORT={"Battery & charging":8,"Performance & crashes":10,"Connectivity & sync":8,"Audio quality":6,"Setup & account":5,"Design & comfort":9,"Delivery & replacement":4,"Other":4}
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"05-topic-modeling"/"outputs"/"feedback_topics.parquet"); total=df.record_id.nunique(); out=df.groupby("topic").agg(volume=("record_id","size"),severity=("severity","mean"),negative_share=("vader_sentiment",lambda s:(s=="negative").mean()),mean_sentiment=("vader_compound","mean")).reset_index(); out["reach"]=out.volume/total; out["impact_weight"]=out.topic.map(IMPACT); out["estimated_revenue_at_risk"]=out.impact_weight*out.volume*85; out["effort_engineer_weeks"]=out.topic.map(EFFORT); out["priority_score"]=(out.reach*.30+out.severity*.30+out.negative_share*.20+out.impact_weight*.20)*100; out["rice_score"]=(out.volume*out.impact_weight*.80)/out.effort_engineer_weeks; out=out.sort_values("priority_score",ascending=False); target=root/"07-product-strategy"/"outputs"; target.mkdir(exist_ok=True); out.to_csv(target/"prioritized_issues.csv",index=False)
 with pd.ExcelWriter(root/"07-product-strategy"/"rice_prioritization.xlsx",engine="openpyxl") as w: out[["topic","volume","impact_weight","effort_engineer_weeks","rice_score","priority_score"]].to_excel(w,index=False,sheet_name="RICE"); ws=w.book["RICE"]; ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
 print(out.head(3)[["topic","priority_score"]].to_string(index=False)); print("So what? The score makes tradeoffs explicit; leaders should still challenge impact assumptions and inspect verbatims before committing capacity.")
if __name__=="__main__": main()

