from pathlib import Path
import re, pandas as pd
ENTITIES={"LUMEN-BUDS-2":r"buds|earbuds|LUMEN-BUDS-2","LUMEN-WATCH-X":r"watch|LUMEN-WATCH-X","LUMEN-HUB-MINI":r"hub|LUMEN-HUB-MINI","LUMEN-APP":r"app|ios|android"}
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"05-topic-modeling"/"outputs"/"feedback_topics.parquet"); df["extracted_entities"]=df.apply(lambda r:"|".join([e for e,p in ENTITIES.items() if re.search(p,r.text,re.I)]) or str(r.product_sku),axis=1); df.to_parquet(root/"06-entity-extraction"/"entity_feedback.parquet",index=False); print("So what? Entity mapping turns generic complaints into accountable product-line work.")
if __name__=="__main__": main()

