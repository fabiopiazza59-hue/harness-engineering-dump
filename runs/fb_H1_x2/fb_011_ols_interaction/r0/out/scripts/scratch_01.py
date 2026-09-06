import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[(df['age']>=18) & (df['age']<=80)]

# drop missing math_score, weight_kg, height_cm
df = df.dropna(subset=['math_score','weight_kg','height_cm'])

# BMI
df['bmi'] = df['weight_kg']/( (df['height_cm']/100)**2 )
df = df[(df['bmi']>=15) & (df['bmi']<=50)]

# exposure coding
df['exposure'] = df['program'].str.strip().str.lower().map({'tutoring':1,'standard':0})

# center age
mean_age = df['age'].mean()
df['age_c'] = df['age'] - mean_age
df['inter'] = df['exposure']*df['age_c']

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
 'r_squared': model.rsquared
}
print(json.dumps(result))
