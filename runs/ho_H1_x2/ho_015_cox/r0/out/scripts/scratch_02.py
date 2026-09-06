import pandas as pd
import numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan).replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df['exposure'] = df['program_norm'].map({'coaching':1, 'waitlist':0})

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. exclude zero followup
df = df[df['followup_days'] != 0]

# 7. administrative censoring at 730
df['event_final'] = df['event']
mask = df['followup_days'] > 730
df.loc[mask, 'followup_days'] = 730
df.loc[mask, 'event_final'] = 0

# 8. drop missing needed columns
cols_needed = ['age','exposure','event_final','followup_days']
df = df.dropna(subset=cols_needed)

n_model = len(df)
n_events = int(df['event_final'].sum())
median_followup = float(df['followup_days'].median())

exog = df[['exposure','age']].astype(float)
model = PHReg(df['followup_days'].astype(float), exog, status=df['event_final'].astype(float), ties='breslow')
result = model.fit()

params = result.params
se = result.bse
pvals = result.pvalues

hr_exposure = float(np.exp(params[0]))
hr_age = float(np.exp(params[1]))

z = 1.96
ci_low_exp = float(np.exp(params[0] - z*se[0]))
ci_high_exp = float(np.exp(params[0] + z*se[0]))
p_exposure = float(pvals[0])

output = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': ci_low_exp,
 'hr_ci_high': ci_high_exp,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}

print(json.dumps(output))
