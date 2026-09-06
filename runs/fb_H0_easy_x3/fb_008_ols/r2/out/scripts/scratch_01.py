import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df.age>=18)&(df.age<=80)]
df = df.dropna(subset=['savings','bmi'])
mean_s = df.savings.mean()
sd_s = df.savings.std(ddof=1)
df = df[(df.savings-mean_s).abs() <= 3*sd_s]
df['exposure'] = (df.program=='coaching').astype(int)

X = df[['exposure','age','bmi','baseline']]
X = sm.add_constant(X)
y = df['savings']
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
