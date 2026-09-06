import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
n0 = len(df)

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# drop missing math_score, weight_kg, height_cm
df = df.dropna(subset=['math_score','weight_kg','height_cm'])

# BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# exposure coding
df['exposure'] = (df['program'].str.strip().str.lower() == 'tutoring').astype(int)

# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['interaction'] = df['exposure'] * df['age_c']

X = df[['exposure','age_c','interaction','bmi']]
X = sm.add_constant(X)
y = df['math_score']

model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': float(model.params['exposure']),
 'se_exposure_hc3': float(model.bse['exposure']),
 'p_exposure': float(model.pvalues['exposure']),
 'coef_interaction': float(model.params['interaction']),
 'p_interaction': float(model.pvalues['interaction']),
 'coef_bmi': float(model.params['bmi']),
 'r_squared': float(model.rsquared)
}
print(json.dumps(result))
