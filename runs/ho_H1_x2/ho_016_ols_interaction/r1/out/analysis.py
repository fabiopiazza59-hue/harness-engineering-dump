import pandas as pd, numpy as np, statsmodels.formula.api as smf, json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 with NaN everywhere
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case on savings weight height
df = df.dropna(subset=['savings','weight_kg','height_cm'])
# BMI
df['bmi'] = df['weight_kg']/((df['height_cm']/100)**2)
df = df[(df['bmi']>=15)&(df['bmi']<=50)]
# exposure
df['exposure'] = (df['program'].str.strip().str.lower()=='coaching').astype(int)
# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean

model = smf.ols('savings ~ exposure + age_c + exposure:age_c + bmi', data=df).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure_hc3': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_interaction': model.params['exposure:age_c'],
 'p_interaction': model.pvalues['exposure:age_c'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
