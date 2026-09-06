import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# age filter
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
# drop missing savings, weight_kg, height_cm
df = df.dropna(subset=['savings','weight_kg','height_cm'])
# BMI
df['bmi'] = df['weight_kg']/((df['height_cm']/100)**2)
df = df[(df['bmi']>=15) & (df['bmi']<=50)]
# exposure
df['exposure'] = df['program'].str.strip().str.lower().map({'coaching':1,'waitlist':0})

age_mean = df['age'].mean()
df['age_c'] = df['age'] - age_mean
df['interaction'] = df['exposure']*df['age_c']

X = df[['exposure','age_c','interaction','bmi']]
X = sm.add_constant(X)
y = df['savings']

model = sm.OLS(y, X).fit(cov_type='HC3')

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
