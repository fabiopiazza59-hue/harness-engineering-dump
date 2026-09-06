import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['rt_ms'] + biomarkers
df = df.dropna(subset=cols)
n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['rt_ms'])
    rs.append(r)
    pvals.append(p)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m)
sorted_p = np.array(pvals)[order]
adj = sorted_p * m / (np.arange(m)+1)
# enforce monotonicity from the end
adj_sorted = np.minimum.accumulate(adj[::-1])[::-1]
adj_sorted = np.clip(adj_sorted, 0, 1)
p_adj = np.empty(m)
p_adj[order] = adj_sorted

out = {}
out['n_analysed'] = n_analysed
for i,b in enumerate(biomarkers):
    out[f'r_{b}'] = rs[i]
    out[f'p_adj_{b}'] = p_adj[i]

n_sig = int(np.sum(p_adj < 0.05))
idx_strongest = int(np.argmax(np.abs(rs)))
r_strongest = rs[idx_strongest]

claims = {
 'n_analysed': n_analysed,
 'r_biomarker_1': rs[0],
 'p_adj_biomarker_1': p_adj[0],
 'r_biomarker_3': rs[2],
 'p_adj_biomarker_3': p_adj[2],
 'p_adj_biomarker_5': p_adj[4],
 'n_significant_adj': n_sig,
 'r_strongest': r_strongest
}
print(json.dumps(claims))
