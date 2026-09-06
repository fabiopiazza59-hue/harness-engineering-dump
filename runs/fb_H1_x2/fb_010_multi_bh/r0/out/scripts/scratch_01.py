import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18)&(df['age']<=80)]
# complete case on savings and biomarkers
cols = ['savings','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)

n_analysed = len(df)

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
rs = {}
ps = {}
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['savings'])
    rs[b]=r
    ps[b]=p

# BH adjustment
pvals = np.array([ps[b] for b in biomarkers])
m = len(pvals)
order = np.argsort(pvals)
ranked = pvals[order]
adj = ranked * m / (np.arange(1,m+1))
# enforce monotonicity from the end
adj = np.minimum.accumulate(adj[::-1])[::-1]
adj = np.clip(adj,0,1)
p_adj_sorted = np.empty(m)
p_adj_sorted[order] = adj
p_adj = {biomarkers[i]: p_adj_sorted[i] for i in range(m)}

n_significant_adj = sum(1 for b in biomarkers if p_adj[b] < 0.05)

strongest = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest]

result = {
 'n_analysed': n_analysed,
 'r_biomarker_1': rs['biomarker_1'],
 'p_adj_biomarker_1': p_adj['biomarker_1'],
 'r_biomarker_3': rs['biomarker_3'],
 'p_adj_biomarker_3': p_adj['biomarker_3'],
 'p_adj_biomarker_5': p_adj['biomarker_5'],
 'n_significant_adj': n_significant_adj,
 'r_strongest': r_strongest,
}
import json
print(json.dumps(result))
