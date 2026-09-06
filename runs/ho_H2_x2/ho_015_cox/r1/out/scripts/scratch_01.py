import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 2. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 3. replace -999 with NaN
df = df.replace(-999, np.nan)

# 4. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# 5. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 6. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 7. exclude zero followup
df = df[df['followup'] != 0]

# 8. administrative censoring at 730
df['event_c'] = df['event']
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event_c'] = 0

# 10. code exposure
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program'] == 'coaching').astype(int)

# 9. drop missing needed vars
needed = ['age','exposure','event_c','followup']
df = df.dropna(subset=needed)

n_model = len(df)
n_events = int(df['event_c'].sum())
median_followup = float(df['followup'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df[['followup','event_c','exposure','age']], duration_col='followup', event_col='event_c')

summary = cph.summary
hr_exposure = float(np.exp(summary.loc['exposure','coef']))
se_exp = summary.loc['exposure','se(coef)']
coef_exp = summary.loc['exposure','coef']
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
p_exposure = float(summary.loc['exposure','p'])
hr_age = float(np.exp(summary.loc['age','coef']))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
print(json.dumps(result))
