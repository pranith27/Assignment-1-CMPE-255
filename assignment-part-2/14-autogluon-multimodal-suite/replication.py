import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import KFold
OUT=Path(__file__).parent/'artifacts'; OUT.mkdir(exist_ok=True); rng=np.random.default_rng(42); n=1200
cats=np.array(['Electronics','Kitchen','Sports','Luxury']); cat=rng.choice(cats,n); rating=rng.uniform(3.5,5,n); condition=rng.choice(['New','Open Box','Used'],n,p=[.45,.25,.30]);
words=np.array(['premium','wireless','portable','professional','compact','smart','stainless','performance','durable']); text=[' '.join(rng.choice(words,size=8,replace=True)) for _ in range(n)]
image=rng.normal(size=(n,12)); image[:,0]+=np.where(cat=='Luxury',1.5,0); image[:,1]+=rating/5
price=150+90*(cat=='Luxury')+45*(cat=='Electronics')+30*(cat=='Sports')+20*rating+30*(condition=='New')+15*image[:,0]+rng.normal(0,12,n)
split=int(.8*n); tfid=TfidfVectorizer(max_features=40); Xt_train=tfid.fit_transform(np.array(text[:split])).toarray(); Xt_test=tfid.transform(np.array(text[split:])).toarray(); Xt=np.vstack([Xt_train,Xt_test]); Xtab=np.column_stack([rating,(condition=='New').astype(int),(condition=='Open Box').astype(int),(cat=='Electronics').astype(int),(cat=='Kitchen').astype(int),(cat=='Sports').astype(int)]); Xs={'text':Xt,'image':image,'tabular':Xtab}; y=price
# Base learners + OOF predictions for leakage-safe stacking
kf=KFold(n_splits=5,shuffle=True,random_state=42); oof={k:np.zeros(split) for k in Xs}; test_pred={}
for name,X in Xs.items():
    Xtr=X[:split]; Xte=X[split:]
    for tr_idx,val_idx in kf.split(Xtr):
        m=Ridge(alpha=5).fit(Xtr[tr_idx],y[:split][tr_idx]); oof[name][val_idx]=m.predict(Xtr[val_idx])
    final=Ridge(alpha=5).fit(Xtr,y[:split]); test_pred[name]=final.predict(Xte)
oof_matrix=np.column_stack([oof['text'],oof['image'],oof['tabular']]); meta=Ridge(alpha=1).fit(oof_matrix,y[:split]); stack_pred=meta.predict(np.column_stack([test_pred['text'],test_pred['image'],test_pred['tabular']]))
ens=(test_pred['text']+test_pred['image']+test_pred['tabular'])/3
rows=[]
for name,pr in [('Text only',test_pred['text']),('Image only',test_pred['image']),('Tabular only',test_pred['tabular']),('Equal-weight fusion',ens),('OOF Ridge stacking',stack_pred)]: rows.append({'model':name,'MAE':mean_absolute_error(y[split:],pr),'R2':r2_score(y[split:],pr)})
pd.DataFrame(rows).to_csv(OUT/'modality_ablation.csv',index=False); pd.DataFrame({'actual':y[split:],'text':test_pred['text'],'image':test_pred['image'],'tabular':test_pred['tabular'],'equal_weight':ens,'oof_stack':stack_pred}).to_csv(OUT/'fusion_predictions.csv',index=False)
plt.figure(figsize=(8,4)); plt.bar([r['model'] for r in rows],[r['MAE'] for r in rows]); plt.xticks(rotation=25,ha='right'); plt.ylabel('MAE'); plt.title('Multimodal Modality Ablation'); plt.tight_layout(); plt.savefig(OUT/'modality_ablation.png',dpi=160); plt.close(); print(pd.DataFrame(rows).round(3).to_string(index=False))
