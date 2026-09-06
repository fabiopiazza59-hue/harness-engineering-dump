import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['glucose_fu'])
mu, sd = df['glucose_fu'].mean(), df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mu).abs() <= 3 * sd]
a = df.loc[df['diet'] == 'usual', 'glucose_fu']
b = df.loc[df['diet'] == 'mediterranean', 'glucose_fu']
res = st.ttest_ind(b, a, equal_var=False)
sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
out = {'n_usual': len(a), 'n_mediterranean': len(b), 'mean_usual': a.mean(), 'mean_mediterranean': b.mean(), 'sd_mediterranean': b.std(ddof=1), 'mean_diff': b.mean()-a.mean(), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_d': (b.mean()-a.mean())/sp}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
