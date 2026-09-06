import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['sbp_12w', 'biomarker_1', 'biomarker_2', 'biomarker_3', 'biomarker_4', 'biomarker_5', 'biomarker_6'])
cols = [f'biomarker_{k}' for k in range(1, 7)]
rp = [st.pearsonr(df[c], df['sbp_12w']) for c in cols]; rs = [x[0] for x in rp]; ps = [x[1] for x in rp]
rej, padj, _, _ = multipletests(ps, alpha=0.05, method='fdr_bh')
strongest = max(range(6), key=lambda i: abs(rs[i]))
out = {'n_analysed': len(df), 'r_biomarker_1': rs[0], 'p_adj_biomarker_1': padj[0], 'r_biomarker_3': rs[2], 'p_adj_biomarker_3': padj[2], 'p_adj_biomarker_5': padj[4], 'n_significant_adj': int(rej.sum()), 'r_strongest': rs[strongest]}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
