import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['sbp_12w'])
    results[b] = {'r': r, 'p': p}

pvals = [results[b]['p'] for b in biomarkers]
m = len(pvals)
order = np.argsort(pvals)
sorted_p = np.array(pvals)[order]
adj = sorted_p * m / (np.arange(1,m+1))
adj_sorted = np.minimum.accumulate(adj[::-1])[::-1]
adj_sorted = np.clip(adj_sorted, 0, 1)
adj_p = np.empty(m)
adj_p[order] = adj_sorted

for i,b in enumerate(biomarkers):
    results[b]['p_adj'] = adj_p[i]

n_significant_adj = sum(1 for b in biomarkers if results[b]['p_adj'] < 0.05)

abs_r = {b: abs(results[b]['r']) for b in biomarkers}
strongest = max(abs_r, key=abs_r.get)
r_strongest = results[strongest]['r']

claims = {
    'n_analysed': n_analysed,
    'r_biomarker_1': results['biomarker_1']['r'],
    'p_adj_biomarker_1': results['biomarker_1']['p_adj'],
    'r_biomarker_3': results['biomarker_3']['r'],
    'p_adj_biomarker_3': results['biomarker_3']['p_adj'],
    'p_adj_biomarker_5': results['biomarker_5']['p_adj'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest
}
print(json.dumps(claims))
