import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['rt_ms'] + biomarkers
df = df.dropna(subset=cols)
n_analysed = len(df)

results = {}
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['rt_ms'])
    results[b] = {'r': r, 'p': p}

pvals = [results[b]['p'] for b in biomarkers]
# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m)
cummin = 1.0
adj = [0]*m
sorted_p = np.array(pvals)[order]
adj_sorted = sorted_p * m / (np.arange(m)+1)
# enforce monotonicity from the largest
for i in range(m-2, -1, -1):
    adj_sorted[i] = min(adj_sorted[i], adj_sorted[i+1])
adj_sorted = np.clip(adj_sorted, 0, 1)
adj_p = np.empty(m)
adj_p[order] = adj_sorted
for i,b in enumerate(biomarkers):
    results[b]['p_adj'] = adj_p[i]

n_significant_adj = sum(1 for b in biomarkers if results[b]['p_adj'] < 0.05)
strongest = max(biomarkers, key=lambda b: abs(results[b]['r']))

claims = {
    'n_analysed': n_analysed,
    'r_biomarker_1': results['biomarker_1']['r'],
    'p_adj_biomarker_1': results['biomarker_1']['p_adj'],
    'r_biomarker_3': results['biomarker_3']['r'],
    'p_adj_biomarker_3': results['biomarker_3']['p_adj'],
    'p_adj_biomarker_5': results['biomarker_5']['p_adj'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': results[strongest]['r']
}
import json
print(json.dumps(claims))
