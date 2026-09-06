import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['savings', 'bmi'])
mu, sd = df['savings'].mean(), df['savings'].std(ddof=1)
df = df[(df['savings'] - mu).abs() <= 3 * sd]
X = pd.DataFrame({'exposure': (df['program'] == 'coaching').astype(float)})
for c in ['age', 'bmi', 'baseline']:
    X[c] = df[c]
X = sm.add_constant(X)
m = sm.OLS(df['savings'], X).fit()
out = {'n_model': int(m.nobs), 'coef_exposure': m.params['exposure'], 'se_exposure': m.bse['exposure'], 'p_exposure': m.pvalues['exposure'], 'coef_age': m.params['age'], 'r_squared': m.rsquared, 'adj_r_squared': m.rsquared_adj}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
