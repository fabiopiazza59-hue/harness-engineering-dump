import pandas as pd, numpy as np, statsmodels.formula.api as smf, json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. filter age 18-80
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. drop missing math_score, weight_kg, height_cm
df = df.dropna(subset=['math_score', 'weight_kg', 'height_cm'])

# 5. compute BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# 6. exposure coding
df['exposure'] = (df['program'].str.strip().str.lower() == 'tutoring').astype(int)

# 7. center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['interaction'] = df['exposure'] * df['age_c']

model = smf.ols('math_score ~ exposure + age_c + interaction + bmi', data=df).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure_hc3': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_interaction': model.params['interaction'],
 'p_interaction': model.pvalues['interaction'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
