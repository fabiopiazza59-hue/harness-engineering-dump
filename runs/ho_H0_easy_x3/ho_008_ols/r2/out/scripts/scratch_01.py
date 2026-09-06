import pandas as pd
import statsmodels.api as sm
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['rt_ms','bmi'])
df['exposure'] = (df['condition']=='caffeine').astype(int)

X = df[['exposure','age','bmi','baseline']]
X = sm.add_constant(X)
y = df['rt_ms']
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
