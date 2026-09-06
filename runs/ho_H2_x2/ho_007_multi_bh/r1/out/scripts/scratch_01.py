import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case on sbp_12w and biomarkers
cols = ['sbp_12w','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)

n_analysed = len(df)

biomarkers = ['biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
results = {}
pvals = []
rs = []
for b in biomarkers:
    r,p = stats.pearsonr(df[b], df['sbp_12w'])
    results[b] = {'r':r,'p':p}
    pvals.append(p)
    rs.append(r)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m)
sorted_p = np.array(pvals)[order]
adj = sorted_p * m / (np.arange(1,m+1))
# enforce monotonicity from the largest down
adj = np.minimum.accumulate(adj[::-1])[::-1]
adj = np.clip(adj, 0, 1)
adj_p = np.empty(m)
adj_p[order] = adj

for i,b in enumerate(biomarkers):
    results[b]['p_adj'] = adj_p[i]

n_sig = sum(1 for b in biomarkers if results[b]['p_adj'] < 0.05)

abs_rs = [abs(results[b]['r']) for b in biomarkers]
strongest_b = biomarkers[int(np.argmax(abs_rs))]
r_strongest = results[strongest_b]['r']

out = {
 'n_analysed': n_analysed,
 'r_biomarker_1': results['biomarker_1']['r'],
 'p_adj_biomarker_1': results['biomarker_1']['p_adj'],
 'r_biomarker_3': results['biomarker_3']['r'],
 'p_adj_biomarker_3': results['biomarker_3']['p_adj'],
 'p_adj_biomarker_5': results['biomarker_5']['p_adj'],
 'n_significant_adj': n_sig,
 'r_strongest': r_strongest
}
print(json.dumps(out))
