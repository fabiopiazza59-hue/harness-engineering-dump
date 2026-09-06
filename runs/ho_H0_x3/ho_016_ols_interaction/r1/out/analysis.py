import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# drop exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case on savings, weight_kg, height_cm
df = df.dropna(subset=['savings','weight_kg','height_cm'])
# BMI
df['bmi'] = df['weight_kg'] / (df['height_cm']/100)**2
df = df[(df['bmi']>=15) & (df['bmi']<=50)]
# program coding
df['program_bin'] = (df['program'].str.strip().str.lower()=='coaching').astype(int)
# center age
age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['inter'] = df['program_bin'] * df['age_c']

X = df[['program_bin','age_c','inter','bmi']]
X = sm.add_constant(X)
y = df['savings']

model = sm.OLS(y, X).fit(cov_type='HC3')

result = {
 'n_model': int(len(df)),
 'coef_exposure': float(model.params['program_bin']),
 'se_exposure_hc3': float(model.bse['program_bin']),
 'p_exposure': float(model.pvalues['program_bin']),
 'coef_interaction': float(model.params['inter']),
 'p_interaction': float(model.pvalues['inter']),
 'coef_bmi': float(model.params['bmi']),
 'r_squared': float(model.rsquared)
}
print(json.dumps(result))
