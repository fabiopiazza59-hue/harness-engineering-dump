import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['sbp_12w'])
tab = pd.crosstab(df['arm'], df['event']).reindex(index=['control', 'treatment'], columns=[0, 1]).fillna(0)
chi2, p, dof, _ = st.chi2_contingency(tab.values, correction=False)
p0 = tab.loc['control', 1] / tab.loc['control'].sum(); p1 = tab.loc['treatment', 1] / tab.loc['treatment'].sum()
out = {'n_control': int(tab.loc['control'].sum()), 'n_treatment': int(tab.loc['treatment'].sum()), 'events_treatment': int(tab.loc['treatment', 1]), 'prop_control': p0, 'prop_treatment': p1, 'risk_ratio': p1/p0, 'chi2_stat': chi2, 'p_value': p}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
