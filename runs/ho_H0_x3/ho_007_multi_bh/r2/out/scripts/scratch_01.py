import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
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

pvals = [ps[b] for b in biomarkers]
rej, padj, _, _ = multipletests(pvals, method='fdr_bh')
padj_dict = dict(zip(biomarkers, padj))

n_significant_adj = int(sum(padj_dict[b] < 0.05 for b in biomarkers))

abs_rs = {b: abs(rs[b]) for b in biomarkers}
strongest = max(abs_rs, key=abs_rs.get)
r_strongest = rs[strongest]

result = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': padj_dict['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': padj_dict['biomarker_3'],
    'p_adj_biomarker_5': padj_dict['biomarker_5'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest
}
print(json.dumps(result))
