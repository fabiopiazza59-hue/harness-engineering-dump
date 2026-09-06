import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates keep first
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
biom = [f'biomarker_{i}' for i in range(1,7)]
cols = ['savings']+biom
df = df.dropna(subset=cols)
n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biom:
    r,p = stats.pearsonr(df[b], df['savings'])
    rs.append(r)
    pvals.append(p)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m, dtype=float)
sorted_p = np.array(pvals)[order]
adj_sorted = sorted_p * m / (np.arange(1,m+1))
# enforce monotonicity from the largest down
for i in range(m-2, -1, -1):
    adj_sorted[i] = min(adj_sorted[i], adj_sorted[i+1])
adj_sorted = np.minimum(adj_sorted, 1.0)
p_adj = np.empty(m)
p_adj[order] = adj_sorted

n_sig = int((p_adj < 0.05).sum())
abs_r = [abs(x) for x in rs]
idx_max = int(np.argmax(abs_r))
r_strongest = rs[idx_max]

out = {
 'n_analysed': n_analysed,
 'r_biomarker_1': rs[0],
 'p_adj_biomarker_1': p_adj[0],
 'r_biomarker_3': rs[2],
 'p_adj_biomarker_3': p_adj[2],
 'p_adj_biomarker_5': p_adj[4],
 'n_significant_adj': n_sig,
 'r_strongest': r_strongest
}
import json
print(json.dumps(out))
