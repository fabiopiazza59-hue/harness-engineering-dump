import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# Exclusion 1: age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# Exclusion 2: drop missing biomass or bmi
df = df.dropna(subset=['biomass','bmi'])

df['exposure'] = (df['treatment'] == 'fertilised').astype(int)

X = df[['exposure','age','bmi','baseline']]
X = sm.add_constant(X)
y = df['biomass']

model = sm.OLS(y, X).fit()

result = {
 'n_model': int(model.nobs),
 'coef_exposure': float(model.params['exposure']),
 'se_exposure': float(model.bse['exposure']),
 'p_exposure': float(model.pvalues['exposure']),
 'coef_age': float(model.params['age']),
 'r_squared': float(model.rsquared),
 'adj_r_squared': float(model.rsquared_adj)
}
print(json.dumps(result))
