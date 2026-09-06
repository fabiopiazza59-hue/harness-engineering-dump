import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import json

df = pd.read_csv('data.csv')

# remove exact duplicate rows, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['rt_ms'] + biomarkers
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['rt_ms'])
    rs.append(r)
    pvals.append(p)

rej, p_adj, _, _ = multipletests(pvals, method='fdr_bh')

claims = {}
claims['n_analysed'] = n_analysed
claims['r_biomarker_1'] = rs[0]
claims['p_adj_biomarker_1'] = p_adj[0]
claims['r_biomarker_3'] = rs[2]
claims['p_adj_biomarker_3'] = p_adj[2]
claims['p_adj_biomarker_5'] = p_adj[4]
claims['n_significant_adj'] = int((p_adj < 0.05).sum())

abs_rs = [abs(r) for r in rs]
idx_max = abs_rs.index(max(abs_rs))
claims['r_strongest'] = rs[idx_max]

print(json.dumps(claims))
