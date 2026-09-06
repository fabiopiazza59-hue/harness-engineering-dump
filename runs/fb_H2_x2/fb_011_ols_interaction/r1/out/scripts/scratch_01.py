import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# drop missing math_score, weight_kg, height_cm
df = df.dropna(subset=['math_score', 'weight_kg', 'height_cm'])

# compute BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# exposure coding
prog_norm = df['program'].astype(str).str.strip().str.lower()
df['exposure'] = (prog_norm == 'tutoring').astype(int)

# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean

model = smf.ols('math_score ~ exposure * age_c + bmi', data=df).fit(cov_type='HC3')

result = {
    'n_model': int(model.nobs),
    'coef_exposure': float(model.params['exposure']),
    'se_exposure_hc3': float(model.bse['exposure']),
    'p_exposure': float(model.pvalues['exposure']),
    'coef_interaction': float(model.params['exposure:age_c']),
    'p_interaction': float(model.pvalues['exposure:age_c']),
    'coef_bmi': float(model.params['bmi']),
    'r_squared': float(model.rsquared),
}
print(json.dumps(result))
