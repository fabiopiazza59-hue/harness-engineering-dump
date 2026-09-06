import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['rt_ms', 'rt_ms_post'])
d = df['rt_ms_post'] - df['rt_ms']
res = st.ttest_rel(df['rt_ms_post'], df['rt_ms'])
pct = (df['rt_ms_post'] - df['rt_ms']) / df['rt_ms'] * 100
out = {'n_pairs': len(df), 'mean_first': df['rt_ms'].mean(), 'mean_second': df['rt_ms_post'].mean(), 'mean_change': d.mean(), 'sd_change': d.std(ddof=1), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_dz': d.mean()/d.std(ddof=1), 'mean_pct_change': pct.mean()}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
