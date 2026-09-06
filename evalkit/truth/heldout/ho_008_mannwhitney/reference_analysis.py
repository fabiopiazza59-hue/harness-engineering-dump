import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['diet'] = df['diet'].str.strip().str.lower()
df = df.dropna(subset=['glucose_fu'])
a = df.loc[df['diet'] == 'usual', 'glucose_fu']; b = df.loc[df['diet'] == 'mediterranean', 'glucose_fu']
res = st.mannwhitneyu(b, a, alternative='two-sided', method='asymptotic', use_continuity=True)
out = {'n_usual': len(a), 'n_mediterranean': len(b), 'median_usual': a.median(), 'median_mediterranean': b.median(), 'median_diff': b.median()-a.median(), 'u_stat': res.statistic, 'p_value': res.pvalue, 'rank_biserial': 1 - 2*res.statistic/(len(a)*len(b))}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
