from pathlib import Path
import pandas as pd
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"06-entity-extraction"/"entity_feedback.parquet"); df["entity"]=df.extracted_entities.str.split("|"); x=df.explode("entity").groupby(["entity","topic","vader_sentiment"]).agg(feedback_count=("record_id","size"),mean_sentiment=("vader_compound","mean")).reset_index(); x.to_csv(root/"06-entity-extraction"/"entity_topic_crosswalk.csv",index=False); print("So what? The crosswalk identifies the product-topic combinations with concentrated negative exposure.")
if __name__=="__main__": main()

