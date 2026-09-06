import pandas as pd, numpy as np, statsmodels.formula.api as smf, json

df = pd.read_csv('data.csv')

# remove exact duplicates keep first
df = df.drop_duplicates(keep='first')

# replace -999 with NaN across all numeric columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# drop missing savings, weight_kg, height_cm
df = df.dropna(subset=['savings','weight_kg','height_cm'])

# BMI
df['bmi'] = df['weight_kg']/(df['height_cm']/100)**2
df = df[(df['bmi']>=15) & (df['bmi']<=50)]

# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean

# program coding
df['program_bin'] = df['program'].str.strip().str.lower().map({'coaching':1,'waitlist':0})

model = smf.ols('savings ~ program_bin * age_c + bmi', data=df).fit(cov_type='HC3')

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['program_bin'],
 'se_exposure_hc3': model.bse['program_bin'],
 'p_exposure': model.pvalues['program_bin'],
 'coef_interaction': model.params['program_bin:age_c'],
 'p_interaction': model.pvalues['program_bin:age_c'],
 'coef_bmi': model.params['bmi'],
 'r_squared': model.rsquared
}
print(json.dumps(result))
