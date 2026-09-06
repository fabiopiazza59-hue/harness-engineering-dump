import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['treatment'] = df['treatment'].str.strip().str.lower()
df = df.dropna(subset=['biomass'])
a = df.loc[df['treatment'] == 'unfertilised', 'biomass']; b = df.loc[df['treatment'] == 'fertilised', 'biomass']
res = st.mannwhitneyu(b, a, alternative='two-sided', method='asymptotic', use_continuity=True)
out = {'n_unfertilised': len(a), 'n_fertilised': len(b), 'median_unfertilised': a.median(), 'median_fertilised': b.median(), 'median_diff': b.median()-a.median(), 'u_stat': res.statistic, 'p_value': res.pvalue, 'rank_biserial': 1 - 2*res.statistic/(len(a)*len(b))}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
