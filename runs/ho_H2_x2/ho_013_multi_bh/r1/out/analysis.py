import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols_needed)

n_analysed = len(df)

rs = {}
ps = {}
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs[b] = r
    ps[b] = p

pvals = [ps[b] for b in biomarkers]
rej, padj, _, _ = multipletests(pvals, method='fdr_bh')
padj_dict = dict(zip(biomarkers, padj))

n_sig = sum(1 for b in biomarkers if padj_dict[b] < 0.05)

strongest = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest]

result = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': padj_dict['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': padj_dict['biomarker_3'],
    'p_adj_biomarker_5': padj_dict['biomarker_5'],
    'n_significant_adj': n_sig,
    'r_strongest': r_strongest
}
print(json.dumps(result))
