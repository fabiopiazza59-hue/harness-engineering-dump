import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
n0 = len(df)

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN across all numeric columns
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. drop missing math_score, weight_kg, height_cm
df = df.dropna(subset=['math_score','weight_kg','height_cm'])

# 5. compute BMI, exclude implausible
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# 6. code exposure
df['exposure'] = (df['program'] == 'tutoring').astype(int)

# 7. center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['inter'] = df['exposure'] * df['age_c']

X = df[['exposure','age_c','inter','bmi']]
X = sm.add_constant(X)
y = df['math_score']

model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure_hc3': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_interaction': model.params['inter'],
 'p_interaction': model.pvalues['inter'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared,
}
print(json.dumps(result))
