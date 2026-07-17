from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Lumen VoC Intelligence",page_icon="💬",layout="wide")
ROOT=Path(__file__).resolve().parents[1]
@st.cache_data
def load():
 feedback=pd.read_parquet(ROOT/"05-topic-modeling"/"outputs"/"feedback_topics.parquet")
 feedback["date"]=pd.to_datetime(feedback.date); feedback["month"]=feedback.date.dt.to_period("M").dt.to_timestamp()
 priority=pd.read_csv(ROOT/"07-product-strategy"/"outputs"/"prioritized_issues.csv")
 releases=pd.read_csv(ROOT/"02-data"/"product_release_calendar.csv",parse_dates=["release_date"])
 experiment=json.loads((ROOT/"08-experiment"/"outputs"/"before_after_results.json").read_text())
 return feedback,priority,releases,experiment
feedback,priority,releases,experiment=load()
st.title("Lumen Voice of Customer Intelligence")
st.caption("50K feedback records · release-aware sentiment · inspectable topic evidence · cached for Community Cloud")

with st.sidebar:
 st.header("Global filters")
 sources=st.multiselect("Source",sorted(feedback.source.unique()),default=sorted(feedback.source.unique()))
 products=st.multiselect("Product",sorted(feedback.product_sku.astype(str).unique()),default=sorted(feedback.product_sku.astype(str).unique()))
 dates=st.date_input("Date range",value=(feedback.date.min().date(),feedback.date.max().date()))
filtered=feedback[feedback.source.isin(sources)&feedback.product_sku.astype(str).isin(products)]
if len(dates)==2: filtered=filtered[(filtered.date>=pd.Timestamp(dates[0]))&(filtered.date<=pd.Timestamp(dates[1]))]

c1,c2,c3,c4=st.columns(4)
c1.metric("Feedback",f"{filtered.record_id.nunique():,}")
c2.metric("Negative share",f"{(filtered.vader_sentiment=='negative').mean():.1%}")
c3.metric("Mean sentiment",f"{filtered.vader_compound.mean():.2f}")
c4.metric("Top priority",priority.iloc[0].topic)

tabs=st.tabs(["Topic explorer","Sentiment & releases","Model disagreement","Prioritization","Raw feedback","Fix validation"])
with tabs[0]:
 st.subheader("Interactive topic explorer")
 topic=st.selectbox("Choose a customer problem",priority.topic.tolist())
 topic_df=filtered[filtered.topic==topic]
 left,right=st.columns([1.5,1])
 monthly=topic_df.groupby("month").agg(volume=("record_id","size"),sentiment=("vader_compound","mean")).reset_index()
 with left:
  st.plotly_chart(px.line(monthly,x="month",y="volume",markers=True,title=f"{topic}: monthly volume"),width="stretch")
  st.plotly_chart(px.line(monthly,x="month",y="sentiment",markers=True,title="Sentiment trend"),width="stretch")
 with right:
  row=priority[priority.topic==topic].iloc[0]
  st.metric("Priority score",f"{row.priority_score:.1f}"); st.metric("Negative share",f"{row.negative_share:.1%}"); st.metric("Estimated exposure",f"${row.estimated_revenue_at_risk:,.0f}")
  st.markdown("#### Customer verbatims")
  samples=topic_df.sort_values("vader_compound").drop_duplicates("text").head(6)
  for _,r in samples.iterrows(): st.markdown(f"> {r.text}\n\n`{r.source}` · sentiment `{r.vader_compound:.2f}`")
with tabs[1]:
 trend=filtered.groupby(["month","source"]).agg(mean_sentiment=("vader_compound","mean")).reset_index(); fig=px.line(trend,x="month",y="mean_sentiment",color="source",markers=True,title="Sentiment trend by source")
 for _,r in releases.iterrows(): fig.add_vline(x=r.release_date,line_dash="dot",line_color="#ef8354",opacity=.65)
 st.plotly_chart(fig,width="stretch"); st.dataframe(releases[["release_date","release_name","release_notes","expected_signal"]],hide_index=True,width="stretch")
 st.info("Release alignment is diagnostic, not causal proof. Investigate exposure and a comparison group before attributing a change.")
with tabs[2]:
 candidates=filtered[filtered.text.str.contains(r"just kidding|love how|but the|not |never",case=False,regex=True)].copy(); candidates["contextual_label"]=candidates.apply(lambda r:"negative" if any(x in r.text.lower() for x in ["just kidding","but the","not ","never"]) else r.vader_sentiment,axis=1); d=candidates[candidates.contextual_label!=candidates.vader_sentiment].drop_duplicates("text").head(30)
 st.write(f"Illustrative disagreement panel: {len(d)} high-risk cases. Run `transformer_sentiment.py` offline to replace the contextual proxy with cached DistilBERT predictions.")
 st.dataframe(d[["text","vader_sentiment","vader_compound","contextual_label","topic"]],hide_index=True,width="stretch")
 st.markdown("**Interpretation:** literal positive words and punctuation can mislead VADER in sarcasm; both approaches collapse different aspect opinions into one label.")
with tabs[3]:
 st.plotly_chart(px.scatter(priority,x="volume",y="severity",size="estimated_revenue_at_risk",color="priority_score",hover_name="topic",title="Issue volume × severity × estimated impact",color_continuous_scale="Reds"),width="stretch")
 st.dataframe(priority[["topic","volume","severity","negative_share","estimated_revenue_at_risk","effort_engineer_weeks","priority_score","rice_score"]],hide_index=True,width="stretch")
with tabs[4]:
 query=st.text_input("Search verbatims")
 sentiment=st.multiselect("Sentiment",["negative","neutral","positive"],default=["negative","neutral","positive"])
 raw=filtered[filtered.vader_sentiment.isin(sentiment)]
 if query: raw=raw[raw.text.str.contains(query,case=False,regex=False)]
 st.dataframe(raw[["date","source","product_sku","star_rating","topic","vader_sentiment","text"]].drop_duplicates().head(1000),hide_index=True,width="stretch",height=520)
with tabs[5]:
 a,b,c=st.columns(3); a.metric("Complaint volume change",f"-{experiment['volume_reduction']:.1%}"); b.metric("Sentiment change",f"+{experiment['sentiment_change']:.2f}"); c.metric("Welch p-value",f"{experiment['welch_p_value']:.4f}")
 st.write(f"Bootstrap 95% CI for sentiment change: **{experiment['ci_95'][0]:.2f} to {experiment['ci_95'][1]:.2f}**")
 st.warning("This is a simulated measurement exercise, not causal evidence. A real launch requires exposure denominators and a credible counterfactual.")
