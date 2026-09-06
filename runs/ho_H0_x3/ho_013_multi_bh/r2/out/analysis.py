import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicate rows, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols_needed)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs.append(r)
    pvals.append(p)

# BH adjustment
from scipy.stats import rankdata
m = len(pvals)
order = np.argsort(pvals)
ranked_p = np.array(pvals)[order]
adj = np.empty(m)
prev = 1.0
for i in range(m-1, -1, -1):
    rank = i+1
    val = ranked_p[i] * m / rank
    prev = min(prev, val)
    adj[i] = prev
adj_p = np.empty(m)
adj_p[order] = adj

for i,b in enumerate(biomarkers):
    results[b] = {'r': rs[i], 'p': pvals[i], 'p_adj': adj_p[i]}

n_sig = int(np.sum(adj_p < 0.05))

idx_strongest = np.argmax(np.abs(rs))
r_strongest = rs[idx_strongest]

out = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs[0],
    'p_adj_biomarker_1': adj_p[0],
    'r_biomarker_3': rs[2],
    'p_adj_biomarker_3': adj_p[2],
    'p_adj_biomarker_5': adj_p[4],
    'n_significant_adj': n_sig,
    'r_strongest': r_strongest
}
print(json.dumps(out))
