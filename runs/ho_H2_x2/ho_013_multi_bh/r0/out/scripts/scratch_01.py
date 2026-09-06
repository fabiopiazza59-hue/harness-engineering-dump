import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols = ['sbp_12w'] + biomarkers
df = df.dropna(subset=cols)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs.append(r)
    pvals.append(p)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m)
sorted_p = np.array(pvals)[order]
adj = sorted_p * m / (np.arange(1,m+1))
# enforce monotonicity from the end
adj_mono = np.minimum.accumulate(adj[::-1])[::-1]
adj_mono = np.clip(adj_mono,0,1)
p_adj = np.empty(m)
p_adj[order] = adj_mono

n_sig = int((p_adj < 0.05).sum())
abs_rs = [abs(x) for x in rs]
idx_strong = int(np.argmax(abs_rs))
r_strongest = rs[idx_strong]

claims = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs[0],
    'p_adj_biomarker_1': p_adj[0],
    'r_biomarker_3': rs[2],
    'p_adj_biomarker_3': p_adj[2],
    'p_adj_biomarker_5': p_adj[4],
    'n_significant_adj': n_sig,
    'r_strongest': r_strongest
}
import json
print(json.dumps(claims))
