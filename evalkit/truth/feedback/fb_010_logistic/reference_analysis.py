import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['savings', 'bmi'])
X = sm.add_constant(pd.DataFrame({'exposure': (df['program'] == 'coaching').astype(float), 'age': df['age'], 'bmi': df['bmi']}))
m = sm.Logit(df['event'], X).fit(disp=0)
ci = m.conf_int().loc['exposure']
out = {'n_model': int(m.nobs), 'n_events': int(df['event'].sum()), 'or_exposure': float(np.exp(m.params['exposure'])), 'or_ci_low': float(np.exp(ci[0])), 'or_ci_high': float(np.exp(ci[1])), 'p_exposure': m.pvalues['exposure'], 'or_age': float(np.exp(m.params['age']))}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
