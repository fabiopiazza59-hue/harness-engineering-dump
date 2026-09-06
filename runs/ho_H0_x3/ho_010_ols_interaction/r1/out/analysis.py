import pandas as pd, numpy as np
import statsmodels.formula.api as smf
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['sbp_12w','weight_kg','height_cm'])
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi']>=15) & (df['bmi']<=50)]
mean_age = df['age'].mean()
df['age_c'] = df['age'] - mean_age
df['arm_bin'] = (df['arm'].str.strip().str.lower()=='treatment').astype(int)

model = smf.ols('sbp_12w ~ arm_bin * age_c + bmi', data=df).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['arm_bin'],
 'se_exposure_hc3': model.bse['arm_bin'],
 'p_exposure': model.pvalues['arm_bin'],
 'coef_interaction': model.params['arm_bin:age_c'],
 'p_interaction': model.pvalues['arm_bin:age_c'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
