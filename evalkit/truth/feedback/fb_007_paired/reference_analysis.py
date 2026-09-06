import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['math_score', 'math_score_post'])
d = df['math_score_post'] - df['math_score']
res = st.ttest_rel(df['math_score_post'], df['math_score'])
pct = (df['math_score_post'] - df['math_score']) / df['math_score'] * 100
out = {'n_pairs': len(df), 'mean_first': df['math_score'].mean(), 'mean_second': df['math_score_post'].mean(), 'mean_change': d.mean(), 'sd_change': d.std(ddof=1), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_dz': d.mean()/d.std(ddof=1), 'mean_pct_change': pct.mean()}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
