import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['sbp_12w', 'sbp_12w_post'])
d = df['sbp_12w_post'] - df['sbp_12w']
res = st.wilcoxon(df['sbp_12w_post'], df['sbp_12w'], zero_method='wilcox', correction=False, method='approx')
pct = (df['sbp_12w_post'] - df['sbp_12w']) / df['sbp_12w'] * 100
out = {'n_pairs': len(df), 'mean_first': df['sbp_12w'].mean(), 'mean_second': df['sbp_12w_post'].mean(), 'mean_change': d.mean(), 'sd_change': d.std(ddof=1), 'w_stat': res.statistic, 'p_value': res.pvalue, 'cohens_dz': d.mean()/d.std(ddof=1), 'mean_pct_change': pct.mean()}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
