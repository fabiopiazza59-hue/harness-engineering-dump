import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['biomass'])
tab = pd.crosstab(df['treatment'], df['event']).reindex(index=['unfertilised', 'fertilised'], columns=[0, 1]).fillna(0)
chi2, p, dof, _ = st.chi2_contingency(tab.values, correction=False)
p0 = tab.loc['unfertilised', 1] / tab.loc['unfertilised'].sum(); p1 = tab.loc['fertilised', 1] / tab.loc['fertilised'].sum()
out = {'n_unfertilised': int(tab.loc['unfertilised'].sum()), 'n_fertilised': int(tab.loc['fertilised'].sum()), 'events_fertilised': int(tab.loc['fertilised', 1]), 'prop_unfertilised': p0, 'prop_fertilised': p1, 'risk_ratio': p1/p0, 'chi2_stat': chi2, 'p_value': p}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
