import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# drop missing savings, weight_kg, height_cm
df = df.dropna(subset=['savings','weight_kg','height_cm'])

# compute BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi'] >= 15) & (df['bmi'] <= 50)]

# encode program
prog_lower = df['program'].str.lower()
df['program_bin'] = prog_lower.apply(lambda x: 1 if 'coach' in x else (0 if 'wait' in x else np.nan))
df = df.dropna(subset=['program_bin'])

# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['interaction'] = df['program_bin'] * df['age_c']

X = df[['program_bin','age_c','interaction','bmi']]
X = sm.add_constant(X)
y = df['savings']

model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
    'n_model': int(model.nobs),
    'coef_exposure': model.params['program_bin'],
    'se_exposure_hc3': model.bse['program_bin'],
    'p_exposure': model.pvalues['program_bin'],
    'coef_interaction': model.params['interaction'],
    'p_interaction': model.pvalues['interaction'],
    'coef_bmi': model.params['bmi'],
    'r_squared': model.rsquared
}

print(json.dumps(result))
