import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
print('initial', len(df))

# 2. remove exact duplicates
df = df.drop_duplicates(keep='first')
print('after dedup', len(df))

# 3. sentinel -999 -> NaN
df = df.replace(-999, np.nan)

# 4. age 18-80 inclusive
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
print('after age filter', len(df))

# 5. normalise program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
print(df['program_norm'].value_counts())
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)
print('after program filter', len(df))

# 6. follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 7. exclude zero follow-up
df = df[df['followup'] != 0]
print('after zero followup excl', len(df))

# 8. administrative censoring at 730
df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# 9. complete case for model vars
model_vars = ['followup','event_final','exposure','age']
df = df.dropna(subset=model_vars)
print('final n', len(df))

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df[['followup','event_final','exposure','age']], duration_col='followup', event_col='event_final')
summary = cph.summary
print(summary)

n_model = len(df)
n_events = int(df['event_final'].sum())
median_followup = float(df['followup'].median())

hr_exposure = float(np.exp(summary.loc['exposure','coef']))
hr_ci_low = float(np.exp(summary.loc['exposure','coef lower 95%']))
hr_ci_high = float(np.exp(summary.loc['exposure','coef upper 95%']))
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
import json
print(json.dumps(result))
