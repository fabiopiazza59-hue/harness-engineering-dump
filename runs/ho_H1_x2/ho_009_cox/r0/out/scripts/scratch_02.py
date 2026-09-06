import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 2. remove exact duplicates
df = df.drop_duplicates(keep='first')

# 3. sentinel -999 -> NaN
df = df.replace(-999, np.nan)

# 4. age 18-80 inclusive
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]

# 5. normalise program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

# 6. follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 7. exclude zero follow-up
df = df[df['followup'] != 0]

# 8. administrative censoring at 730
df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# 9. complete case
model_vars = ['followup','event_final','exposure','age']
df = df.dropna(subset=model_vars)

print('final n', len(df))

model = PHReg(df['followup'], df[['exposure','age']], status=df['event_final'], ties='breslow')
result = model.fit()
print(result.summary())

params = result.params
bse = result.bse
pvals = result.pvalues

hr_exposure = float(np.exp(params['exposure']))
se_exp = bse['exposure']
hr_ci_low = float(np.exp(params['exposure'] - 1.96*se_exp))
hr_ci_high = float(np.exp(params['exposure'] + 1.96*se_exp))
p_exposure = float(pvals['exposure'])
hr_age = float(np.exp(params['age']))

n_model = len(df)
n_events = int(df['event_final'].sum())
median_followup = float(df['followup'].median())

out = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
print(json.dumps(out))
