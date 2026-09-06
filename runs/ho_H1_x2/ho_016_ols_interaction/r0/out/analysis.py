import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# 3. age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. drop missing savings, weight_kg, height_cm
df = df.dropna(subset=['savings','weight_kg','height_cm'])
# 5. compute BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi']>=15) & (df['bmi']<=50)]
# 6. recode program
df['program_bin'] = (df['program']=='coaching').astype(int)
# 7. center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['inter'] = df['program_bin'] * df['age_c']

X = df[['program_bin','age_c','inter','bmi']]
X = sm.add_constant(X)
y = df['savings']
model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['program_bin'],
 'se_exposure_hc3': model.bse['program_bin'],
 'p_exposure': model.pvalues['program_bin'],
 'coef_interaction': model.params['inter'],
 'p_interaction': model.pvalues['inter'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
