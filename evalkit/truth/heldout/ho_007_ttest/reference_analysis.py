import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['biomass'])
mu, sd = df['biomass'].mean(), df['biomass'].std(ddof=1)
df = df[(df['biomass'] - mu).abs() <= 3 * sd]
a = df.loc[df['treatment'] == 'unfertilised', 'biomass']
b = df.loc[df['treatment'] == 'fertilised', 'biomass']
res = st.ttest_ind(b, a, equal_var=True)
sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
out = {'n_unfertilised': len(a), 'n_fertilised': len(b), 'mean_unfertilised': a.mean(), 'mean_fertilised': b.mean(), 'sd_fertilised': b.std(ddof=1), 'mean_diff': b.mean()-a.mean(), 't_stat': res.statistic, 'p_value': res.pvalue, 'cohens_d': (b.mean()-a.mean())/sp}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
