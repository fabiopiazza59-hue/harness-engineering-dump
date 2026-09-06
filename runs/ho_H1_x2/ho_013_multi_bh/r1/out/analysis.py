import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates keep first
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)
# filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols_needed)

n_analysed = len(df)

results = {}
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['sbp_12w'])
    results[b] = {'r': r, 'p': p}

pvals = [results[b]['p'] for b in biomarkers]
# BH adjustment
from statsmodels.stats.multitest import multipletests
rej, padj, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
for b, pa, rj in zip(biomarkers, padj, rej):
    results[b]['p_adj'] = pa
    results[b]['sig'] = bool(rj)

n_significant_adj = sum(1 for b in biomarkers if results[b]['sig'])

# strongest
strongest_b = max(biomarkers, key=lambda b: abs(results[b]['r']))
r_strongest = results[strongest_b]['r']

out = {
 'n_analysed': n_analysed,
 'r_biomarker_1': results['biomarker_1']['r'],
 'p_adj_biomarker_1': results['biomarker_1']['p_adj'],
 'r_biomarker_3': results['biomarker_3']['r'],
 'p_adj_biomarker_3': results['biomarker_3']['p_adj'],
 'p_adj_biomarker_5': results['biomarker_5']['p_adj'],
 'n_significant_adj': n_significant_adj,
 'r_strongest': r_strongest
}
import json
print(json.dumps(out))
