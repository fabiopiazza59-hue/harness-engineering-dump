import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first').copy()

# 2. -999 -> NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalize condition
df['condition_norm'] = df['condition'].astype(str).str.strip().str.lower()
print(df['condition_norm'].unique())

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. administrative censoring at 730
df['event_c'] = df['event']
mask_long = df['followup'] > 730
df.loc[mask_long, 'followup'] = 730
df.loc[mask_long, 'event_c'] = 0

# 7. exclude followup==0
df = df[df['followup'] != 0]

# 8. exposure coding
df = df[df['condition_norm'].isin(['placebo','caffeine'])]
df['exposure'] = (df['condition_norm'] == 'caffeine').astype(int)

# drop missing age/exposure/followup/event
df = df.dropna(subset=['age','exposure','followup','event_c'])

print(df.shape)
print(df['event_c'].value_counts())
print(df['followup'].describe())

n_model = len(df)
n_events = int(df['event_c'].sum())
median_followup = float(df['followup'].median())

exog = df[['exposure','age']].astype(float)
model = PHReg(df['followup'].astype(float), exog, status=df['event_c'].astype(float), ties='breslow')
result = model.fit()
print(result.summary())

params = result.params
se = result.bse
z = 1.96
coef_exp = params[0]
coef_age = params[1]
se_exp = se[0]

hr_exposure = np.exp(coef_exp)
hr_ci_low = np.exp(coef_exp - z*se_exp)
hr_ci_high = np.exp(coef_exp + z*se_exp)
p_exposure = result.pvalues[0]
hr_age = np.exp(coef_age)

out = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(hr_ci_low),
 'hr_ci_high': float(hr_ci_high),
 'p_exposure': float(p_exposure),
 'hr_age': float(hr_age)
}
print(json.dumps(out))
