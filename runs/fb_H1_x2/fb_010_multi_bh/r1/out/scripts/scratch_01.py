import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

biomarkers = [f'biomarker_{i}' for i in range(1,7)]
cols_needed = ['savings'] + biomarkers
df = df.dropna(subset=cols_needed)

n_analysed = len(df)

results = {}
pvals = []
rs = []
for b in biomarkers:
    r, p = stats.pearsonr(df[b], df['savings'])
    rs.append(r)
    pvals.append(p)

# BH adjustment
m = len(pvals)
order = np.argsort(pvals)
ranked = np.empty(m, dtype=float)
sorted_p = np.array(pvals)[order]
adj_sorted = np.empty(m)
prev = 1.0
for i in range(m-1, -1, -1):
    rank = i+1
    val = sorted_p[i] * m / rank
    prev = min(prev, val)
    adj_sorted[i] = prev
adj = np.empty(m)
adj[order] = adj_sorted
adj = np.clip(adj, 0, 1)

for i,b in enumerate(biomarkers):
    results[b] = {'r': rs[i], 'p': pvals[i], 'p_adj': adj[i]}

abs_rs = [abs(r) for r in rs]
idx_strong = int(np.argmax(abs_rs))
r_strongest = rs[idx_strong]

n_sig = int(sum(1 for a in adj if a < 0.05))

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
