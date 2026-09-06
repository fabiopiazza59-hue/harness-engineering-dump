import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['sbp_12w','weight_kg','height_cm'])
df['bmi'] = df['weight_kg']/((df['height_cm']/100)**2)
df = df[(df['bmi']>=15) & (df['bmi']<=50)]
df['exposure'] = (df['arm']=='treatment').astype(int)
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['inter'] = df['exposure']*df['age_c']

X = df[['exposure','age_c','inter','bmi']]
X = sm.add_constant(X)
y = df['sbp_12w']
model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure_hc3': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_interaction': model.params['inter'],
 'p_interaction': model.pvalues['inter'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
