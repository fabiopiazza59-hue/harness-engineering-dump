import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case on sbp_12w and biomarkers
cols = ['sbp_12w','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)

n_analysed = len(df)

biomarkers = ['biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
rs = {}
ps = {}
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['sbp_12w'])
    rs[b]=r
    ps[b]=p

# BH adjustment
pvals = np.array([ps[b] for b in biomarkers])
n = len(pvals)
order = np.argsort(pvals)
ranked = pvals[order]
adj = np.empty(n)
prev = 1.0
for i in range(n-1, -1, -1):
    val = ranked[i]*n/(i+1)
    prev = min(prev, val)
    adj[i] = prev
adj_p = np.empty(n)
adj_p[order] = adj
adj_p = np.clip(adj_p, 0, 1)

adj_dict = {biomarkers[i]: adj_p[i] for i in range(n)}

n_significant_adj = int(sum(1 for b in biomarkers if adj_dict[b] < 0.05))

abs_rs = {b: abs(rs[b]) for b in biomarkers}
strongest = max(abs_rs, key=abs_rs.get)
r_strongest = rs[strongest]

result = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': adj_dict['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': adj_dict['biomarker_3'],
    'p_adj_biomarker_5': adj_dict['biomarker_5'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest
}
import json
print(json.dumps(result))
