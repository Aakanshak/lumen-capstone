from pathlib import Path
import json, numpy as np, pandas as pd
from scipy.stats import ttest_ind
SEED=42
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"05-topic-modeling"/"outputs"/"feedback_topics.parquet"); b=df[df.topic=="Battery & charging"].copy(); fix=pd.Timestamp("2026-02-01"); before=b[(b.date>=fix-pd.Timedelta(days=90))&(b.date<fix)]; after=b[(b.date>=fix)&(b.date<fix+pd.Timedelta(days=90))].copy(); rng=np.random.default_rng(SEED); after["simulated_post_fix_sentiment"]=(after.vader_compound+rng.normal(.28,.08,len(after))).clip(-1,1); keep=rng.random(len(after))>.38; after_reduced=after[keep]
 stat,p=ttest_ind(before.vader_compound,after_reduced.simulated_post_fix_sentiment,equal_var=False); boot=[]
 for _ in range(2000): boot.append(rng.choice(after_reduced.simulated_post_fix_sentiment,len(after_reduced),replace=True).mean()-rng.choice(before.vader_compound,len(before),replace=True).mean())
 result={"fix_date":str(fix.date()),"before_volume":len(before),"after_volume_simulated":len(after_reduced),"volume_reduction":round(1-len(after_reduced)/max(len(before),1),4),"before_mean_sentiment":round(before.vader_compound.mean(),4),"after_mean_sentiment":round(after_reduced.simulated_post_fix_sentiment.mean(),4),"sentiment_change":round(after_reduced.simulated_post_fix_sentiment.mean()-before.vader_compound.mean(),4),"ci_95":[round(x,4) for x in np.quantile(boot,[.025,.975])],"welch_p_value":round(float(p),6)}; target=root/"08-experiment"/"outputs"; target.mkdir(exist_ok=True); (target/"before_after_results.json").write_text(json.dumps(result,indent=2)); pd.concat([before.assign(period="before",analysis_sentiment=before.vader_compound),after_reduced.assign(period="after",analysis_sentiment=after_reduced.simulated_post_fix_sentiment)]).to_csv(target/"before_after_feedback.csv",index=False); print(result); print("So what? The simulation demonstrates measurement design, not causal proof; a real rollout needs a valid counterfactual and exposure denominator.")
if __name__=="__main__": main()

