import pandas as pd, numpy as np, json
from scipy import stats
from statsmodels.stats.multitest import multipletests

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18)&(df['age']<=80)]
cols = ['savings','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)
n = len(df)

biomarkers = ['biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
rs = []
ps = []
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['savings'])
    rs.append(r)
    ps.append(p)

reject, p_adj, _, _ = multipletests(ps, method='fdr_bh')

results = dict(zip(biomarkers, zip(rs, p_adj)))
n_sig = int(sum(p<0.05 for p in p_adj))
abs_rs = [abs(r) for r in rs]
idx_max = abs_rs.index(max(abs_rs))
r_strongest = rs[idx_max]

out = {
 'n_analysed': n,
 'r_biomarker_1': results['biomarker_1'][0],
 'p_adj_biomarker_1': results['biomarker_1'][1],
 'r_biomarker_3': results['biomarker_3'][0],
 'p_adj_biomarker_3': results['biomarker_3'][1],
 'p_adj_biomarker_5': results['biomarker_5'][1],
 'n_significant_adj': n_sig,
 'r_strongest': r_strongest
}
print(json.dumps(out))
