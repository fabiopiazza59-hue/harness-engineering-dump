import pandas as pd, numpy as np, statsmodels.formula.api as smf, json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. drop rows missing sbp_12w, weight_kg, height_cm
df = df.dropna(subset=['sbp_12w', 'weight_kg', 'height_cm'])

# 5. compute BMI, exclude implausible
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# 6. exposure coding
df['exposure'] = df['arm'].str.strip().str.lower().map({'treatment':1, 'control':0})
df = df.dropna(subset=['exposure'])

# 7. center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean

# 8. fit OLS with HC3
model = smf.ols('sbp_12w ~ exposure + age_c + exposure:age_c + bmi', data=df).fit(cov_type='HC3')

result = {
    'n_model': int(model.nobs),
    'coef_exposure': float(model.params['exposure']),
    'se_exposure_hc3': float(model.bse['exposure']),
    'p_exposure': float(model.pvalues['exposure']),
    'coef_interaction': float(model.params['exposure:age_c']),
    'p_interaction': float(model.pvalues['exposure:age_c']),
    'coef_bmi': float(model.params['bmi']),
    'r_squared': float(model.rsquared)
}
print(json.dumps(result))
