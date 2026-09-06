import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
cols = ['savings','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)
n_analysed = len(df)

biomarkers = ['biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
rs = {}
ps = {}
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['savings'])
    rs[b] = r
    ps[b] = p

# BH adjustment
pvals = np.array([ps[b] for b in biomarkers])
m = len(pvals)
order = np.argsort(pvals)
ranked = pvals[order]
adj = np.empty(m)
prev = 1.0
for i in range(m-1, -1, -1):
    val = ranked[i] * m / (i+1)
    prev = min(prev, val)
    adj[i] = prev
adj_p = np.empty(m)
adj_p[order] = adj
adj_p = np.clip(adj_p, 0, 1)

padj = {b: adj_p[i] for i,b in enumerate(biomarkers)}

n_significant_adj = int(sum(1 for b in biomarkers if padj[b] < 0.05))

strongest = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest]

result = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': padj['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': padj['biomarker_3'],
    'p_adj_biomarker_5': padj['biomarker_5'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest
}
print(json.dumps(result))
