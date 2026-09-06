import pandas as pd, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df.dropna(subset=['biomass','bmi'])
df['exposure'] = (df['treatment']=='fertilised').astype(int)

X = df[['exposure','age','bmi','baseline']]
X = sm.add_constant(X)
y = df['biomass']
model = sm.OLS(y, X).fit()

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_age': model.params['age'],
 'r_squared': model.rsquared,
 'adj_r_squared': model.rsquared_adj
}
print(json.dumps(result))
