import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicate rows, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. complete case on sbp_12w and biomarkers
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
rs = {}
ps = {}
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs[b] = r
    ps[b] = p

pvals = [ps[b] for b in biomarkers]
rej, p_adj, _, _ = multipletests(pvals, method='fdr_bh')
p_adj_dict = dict(zip(biomarkers, p_adj))

n_sig = sum(p_adj_dict[b] < 0.05 for b in biomarkers)

strongest_b = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest_b]

out = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': p_adj_dict['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': p_adj_dict['biomarker_3'],
    'p_adj_biomarker_5': p_adj_dict['biomarker_5'],
    'n_significant_adj': n_sig,
    'r_strongest': r_strongest
}
print(json.dumps(out))
