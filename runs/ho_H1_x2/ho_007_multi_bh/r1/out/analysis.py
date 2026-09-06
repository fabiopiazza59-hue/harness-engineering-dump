import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. complete case on sbp_12w and biomarkers
cols = ['sbp_12w','biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
df = df.dropna(subset=cols)

n_analysed = len(df)

biomarkers = ['biomarker_1','biomarker_2','biomarker_3','biomarker_4','biomarker_5','biomarker_6']
rs = {}
ps = {}
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['sbp_12w'])
    rs[b] = r
    ps[b] = p

# BH adjustment
pvals = np.array([ps[b] for b in biomarkers])
n = len(pvals)
order = np.argsort(pvals)
ranked = pvals[order]
adj = ranked * n / (np.arange(n)+1)
# enforce monotonicity from the largest down
adj = np.minimum.accumulate(adj[::-1])[::-1]
adj = np.clip(adj, 0, 1)
padj_sorted = np.empty(n)
padj_sorted[order] = adj
padj = {biomarkers[i]: padj_sorted[i] for i in range(n)}

n_significant_adj = sum(1 for b in biomarkers if padj[b] < 0.05)

# strongest
strongest_b = max(biomarkers, key=lambda b: abs(rs[b]))
r_strongest = rs[strongest_b]

result = {
    'n_analysed': n_analysed,
    'r_biomarker_1': rs['biomarker_1'],
    'p_adj_biomarker_1': padj['biomarker_1'],
    'r_biomarker_3': rs['biomarker_3'],
    'p_adj_biomarker_3': padj['biomarker_3'],
    'p_adj_biomarker_5': padj['biomarker_5'],
    'n_significant_adj': n_significant_adj,
    'r_strongest': r_strongest
}

print(json.dumps(result))
