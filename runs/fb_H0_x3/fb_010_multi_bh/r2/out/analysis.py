import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['savings'] + biomarkers
df = df.dropna(subset=cols_needed)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['savings'])
    rs.append(r)
    pvals.append(p)

reject, p_adj, _, _ = multipletests(pvals, method='fdr_bh')

out = {}
out['n_analysed'] = n_analysed
for i,b in enumerate(biomarkers):
    out[f'r_{b}'] = rs[i]
    out[f'p_adj_{b}'] = p_adj[i]

out['n_significant_adj'] = int(sum(p_adj < 0.05))
idx_max = np.argmax(np.abs(rs))
out['r_strongest'] = rs[idx_max]

final = {
 'n_analysed': out['n_analysed'],
 'r_biomarker_1': out['r_biomarker_1'],
 'p_adj_biomarker_1': out['p_adj_biomarker_1'],
 'r_biomarker_3': out['r_biomarker_3'],
 'p_adj_biomarker_3': out['p_adj_biomarker_3'],
 'p_adj_biomarker_5': out['p_adj_biomarker_5'],
 'n_significant_adj': out['n_significant_adj'],
 'r_strongest': out['r_strongest'],
}
print(json.dumps(final))
