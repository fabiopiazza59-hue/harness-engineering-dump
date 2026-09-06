import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. complete case on rt_ms and biomarkers
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['rt_ms'] + biomarkers
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['rt_ms'])
    results[b] = {'r': r, 'p': p}
    pvals.append(p)
    rs.append(r)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m, dtype=float)
sorted_p = np.array(pvals)[order]
adj_sorted = sorted_p * m / (np.arange(1, m+1))
# enforce monotonicity (from the largest down)
for i in range(m-2, -1, -1):
    adj_sorted[i] = min(adj_sorted[i], adj_sorted[i+1])
adj_sorted = np.minimum(adj_sorted, 1.0)
adj = np.empty(m, dtype=float)
adj[order] = adj_sorted

for i, b in enumerate(biomarkers):
    results[b]['p_adj'] = adj[i]

n_significant_adj = int(np.sum(adj < 0.05))

abs_rs = [abs(x) for x in rs]
idx_strong = int(np.argmax(abs_rs))
r_strongest = rs[idx_strong]

out = {
    'n_analysed': n_analysed,
    'r_biomarker_1': results['biomarker_1']['r'],
    'p_adj_biomarker_1': results['biomarker_1']['p_adj'],
    'r_biomarker_3': results['biomarker_3']['r'],
    'p_adj_biomarker_3': results['biomarker_3']['p_adj'],
    'p_adj_biomarker_5': results['biomarker_5']['p_adj'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest,
}
print(json.dumps(out))
