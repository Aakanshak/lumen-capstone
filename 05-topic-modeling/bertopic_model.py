"""Modern embedding topic model; run offline and cache outputs."""
from pathlib import Path
import pandas as pd
def main():
 from bertopic import BERTopic
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"03-preprocessing"/"outputs"/"clean_feedback.parquet"); model=BERTopic(min_topic_size=100,calculate_probabilities=False,verbose=True); topics,_=model.fit_transform(df.text.tolist()); df["bertopic_id"]=topics
 target=root/"05-topic-modeling"/"outputs"; target.mkdir(exist_ok=True); df[["record_id","bertopic_id"]].to_csv(target/"bertopic_assignments.csv",index=False); model.get_topic_info().to_csv(target/"bertopic_info.csv",index=False); model.save(target/"bertopic_model",serialization="safetensors")
 print("So what? Embedding clusters better preserve customer phrasing, but labels still require human validation and stability checks.")
if __name__=="__main__": main()

