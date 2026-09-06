import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')
# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# 3. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# 4. complete case on sbp_12w and biomarker_1..6
cols = ['sbp_12w'] + [f'biomarker_{i}' for i in range(1,7)]
df = df.dropna(subset=cols)

n_analysed = len(df)

res = {}
rs = {}
ps = {}
for i in range(1,7):
    b = f'biomarker_{i}'
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs[b] = r
    ps[b] = p

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
pvals = [ps[b] for b in biomarkers]
reject, padj, _, _ = multipletests(pvals, method='fdr_bh')
padj_dict = dict(zip(biomarkers, padj))

n_sig = sum(1 for b in biomarkers if padj_dict[b] < 0.05)

strongest = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest]

claims = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': padj_dict['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': padj_dict['biomarker_3'],
    'p_adj_biomarker_5': padj_dict['biomarker_5'],
    'n_significant_adj': n_sig,
    'r_strongest': r_strongest,
}
print(json.dumps(claims))
