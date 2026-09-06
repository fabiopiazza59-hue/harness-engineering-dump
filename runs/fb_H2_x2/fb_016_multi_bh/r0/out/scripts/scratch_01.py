import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['rt_ms'] + biomarkers
df = df.dropna(subset=cols_needed)
n_analysed = len(df)

results = {}
ps = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['rt_ms'])
    results[b] = (r,p)
    ps.append(p)
    rs.append(r)

# BH adjustment
m = len(ps)
order = np.argsort(ps)
ranked = np.empty(m)
sorted_p = np.array(ps)[order]
adj = sorted_p * m / (np.arange(1,m+1))
# enforce monotonicity from the end
adj_sorted = np.minimum.accumulate(adj[::-1])[::-1]
adj_sorted = np.clip(adj_sorted, 0, 1)
p_adj = np.empty(m)
p_adj[order] = adj_sorted

p_adj_dict = dict(zip(biomarkers, p_adj))

n_sig = int(np.sum(p_adj < 0.05))
abs_rs = [abs(r) for r in rs]
idx_max = int(np.argmax(abs_rs))
r_strongest = rs[idx_max]

claims = {
 'n_analysed': n_analysed,
 'r_biomarker_1': results['biomarker_1'][0],
 'p_adj_biomarker_1': p_adj_dict['biomarker_1'],
 'r_biomarker_3': results['biomarker_3'][0],
 'p_adj_biomarker_3': p_adj_dict['biomarker_3'],
 'p_adj_biomarker_5': p_adj_dict['biomarker_5'],
 'n_significant_adj': n_sig,
 'r_strongest': r_strongest,
}
print(json.dumps(claims))
