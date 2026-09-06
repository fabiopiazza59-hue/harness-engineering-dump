import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
print('initial', len(df))

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
print('after dedup', len(df))

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', len(df))

# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
print(df['program_norm'].value_counts())
df['exposure'] = (df['program_norm']=='coaching').astype(int)

# 5. followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup'] != 0]
print('after zero followup exclusion', len(df))

# administrative censoring at 730
df['event_cens'] = df['event']
df.loc[df['followup']>730, 'event_cens'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# need complete case for age, exposure
df_model = df.dropna(subset=['age','exposure','followup','event_cens'])
print('final model n', len(df_model))

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df_model[['followup','event_cens','exposure','age']], duration_col='followup', event_col='event_cens')

summary = cph.summary
print(summary)

n_model = len(df_model)
n_events = int(df_model['event_cens'].sum())
median_followup = float(df_model['followup'].median())

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
import json
print(json.dumps(result))
