import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 2. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 3. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 4. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 5. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['tutoring','standard'])]
df['exposure'] = (df['program_norm'] == 'tutoring').astype(int)

# 6. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['fup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 7. exclude zero follow-up
df = df[df['fup_days'] > 0]

# 8. administrative censoring at 730
df['event_c'] = df['event']
df.loc[df['fup_days'] > 730, 'event_c'] = 0
df['fup_days_c'] = df['fup_days'].clip(upper=730)

# 9. drop missing in model vars
model_df = df.dropna(subset=['age','exposure','event_c','fup_days_c'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['fup_days_c','event_c','exposure','age']], duration_col='fup_days_c', event_col='event_c')

summary = cph.summary

n_model = int(len(model_df))
n_events = int(model_df['event_c'].sum())
median_followup = float(model_df['fup_days_c'].median())

hr_exposure = float(np.exp(summary.loc['exposure','coef']))
hr_ci_low = float(np.exp(summary.loc['exposure','coef'] - 1.96*summary.loc['exposure','se(coef)']))
hr_ci_high = float(np.exp(summary.loc['exposure','coef'] + 1.96*summary.loc['exposure','se(coef)']))
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
