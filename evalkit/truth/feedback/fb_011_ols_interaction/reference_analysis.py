import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['math_score', 'weight_kg', 'height_cm'])
df = df.assign(bmi=df['weight_kg'] / (df['height_cm']/100)**2)
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]
df = df.assign(age_c=df['age'] - df['age'].mean(), exposure=(df['program'] == 'tutoring').astype(float))
df = df.assign(inter=df['exposure']*df['age_c'])
X = sm.add_constant(df[['exposure', 'age_c', 'inter', 'bmi']])
m = sm.OLS(df['math_score'], X).fit(cov_type='HC3')
out = {'n_model': int(m.nobs), 'coef_exposure': m.params['exposure'], 'se_exposure_hc3': m.bse['exposure'], 'p_exposure': m.pvalues['exposure'], 'coef_interaction': m.params['inter'], 'p_interaction': m.pvalues['inter'], 'coef_bmi': m.params['bmi'], 'r_squared': m.rsquared}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
