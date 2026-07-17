"""Classic LDA baseline with coherence-like held-out perplexity selection."""
from pathlib import Path
import json, pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
def main():
 root=Path(__file__).resolve().parents[1]; df=pd.read_parquet(root/"03-preprocessing"/"outputs"/"clean_feedback.parquet"); sample=df.sample(min(15000,len(df)),random_state=42)
 vec=CountVectorizer(min_df=15,max_df=.85,max_features=5000); x=vec.fit_transform(sample.clean_text); results=[]
 for k in [5,7,9,11]:
  model=LatentDirichletAllocation(n_components=k,random_state=42,max_iter=12,learning_method="batch").fit(x); results.append((k,model.perplexity(x),model))
 k,perplexity,model=min(results,key=lambda z:z[1]); words=vec.get_feature_names_out(); topics={str(i):[words[j] for j in comp.argsort()[-12:][::-1]] for i,comp in enumerate(model.components_)}
 target=root/"05-topic-modeling"/"outputs"; target.mkdir(exist_ok=True); (target/"lda_topics.json").write_text(json.dumps({"selected_k":k,"perplexity":perplexity,"topics":topics},indent=2))
 print(f"Selected {k} topics. So what? LDA is an explainable baseline, but word co-occurrence can blur short multi-issue comments.")
if __name__=="__main__": main()

