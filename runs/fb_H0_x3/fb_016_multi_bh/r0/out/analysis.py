import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# drop exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case on rt_ms and biomarkers
cols = ['rt_ms'] + [f'biomarker_{i}' for i in range(1,7)]
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
rs = {}
ps = {}
for i in range(1,7):
    b = f'biomarker_{i}'
    r, p = stats.pearsonr(df[b], df['rt_ms'])
    rs[b] = r
    ps[b] = p

# BH adjustment
names = [f'biomarker_{i}' for i in range(1,7)]
pvals = np.array([ps[n] for n in names])
m = len(pvals)
order = np.argsort(pvals)
ranked = pvals[order]
adj = ranked * m / (np.arange(m)+1)
# enforce monotonicity from the largest down
adj = np.minimum.accumulate(adj[::-1])[::-1]
adj = np.clip(adj, 0, 1)
p_adj = np.empty(m)
p_adj[order] = adj
p_adj_dict = dict(zip(names, p_adj))

n_significant_adj = int(np.sum(p_adj < 0.05))

abs_r = {n: abs(rs[n]) for n in names}
strongest = max(abs_r, key=abs_r.get)
r_strongest = rs[strongest]

out = {
 'n_analysed': n_analysed,
 'r_biomarker_1': rs['biomarker_1'],
 'p_adj_biomarker_1': p_adj_dict['biomarker_1'],
 'r_biomarker_3': rs['biomarker_3'],
 'p_adj_biomarker_3': p_adj_dict['biomarker_3'],
 'p_adj_biomarker_5': p_adj_dict['biomarker_5'],
 'n_significant_adj': n_significant_adj,
 'r_strongest': r_strongest
}
print(json.dumps(out))
