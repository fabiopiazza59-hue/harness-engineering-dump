import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['rt_ms'])
mu, sd = df['rt_ms'].mean(), df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mu).abs() <= 3 * sd]
a = df.loc[df['condition'] == 'placebo', 'rt_ms']
b = df.loc[df['condition'] == 'caffeine', 'rt_ms']
res = st.ttest_ind(b, a, equal_var=False)
sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
out = {'n_placebo': len(a), 'n_caffeine': len(b), 'mean_placebo': a.mean(), 'mean_caffeine': b.mean(), 'sd_caffeine': b.std(ddof=1), 'mean_diff': b.mean()-a.mean(), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_d': (b.mean()-a.mean())/sp}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
