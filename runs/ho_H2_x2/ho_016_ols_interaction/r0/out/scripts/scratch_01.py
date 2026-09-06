import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18)&(df['age']<=80)]
df = df.dropna(subset=['savings','weight_kg','height_cm'])
df['bmi'] = df['weight_kg']/((df['height_cm']/100)**2)
df = df[(df['bmi']>=15)&(df['bmi']<=50)]
df['exposure'] = (df['program'].str.strip().str.lower()=='coaching').astype(int)
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['inter'] = df['exposure']*df['age_c']

X = df[['exposure','age_c','inter','bmi']]
X = sm.add_constant(X)
y = df['savings']
model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(len(df)),
 'coef_exposure': float(model.params['exposure']),
 'se_exposure_hc3': float(model.bse['exposure']),
 'p_exposure': float(model.pvalues['exposure']),
 'coef_interaction': float(model.params['inter']),
 'p_interaction': float(model.pvalues['inter']),
 'coef_bmi': float(model.params['bmi']),
 'r_squared': float(model.rsquared)
}
print(json.dumps(result))
