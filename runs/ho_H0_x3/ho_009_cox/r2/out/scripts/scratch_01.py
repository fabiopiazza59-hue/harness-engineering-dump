import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

# 5. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup'] != 0]

# administrative censoring at 730
df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# drop missing needed columns
cols_needed = ['age','exposure','event_final','followup']
df_model = df.dropna(subset=cols_needed).copy()

n_model = len(df_model)
n_events = int(df_model['event_final'].sum())
median_followup = float(df_model['followup'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df_model[['followup','event_final','exposure','age']], duration_col='followup', event_col='event_final')

summ = cph.summary
hr_exposure = float(np.exp(summ.loc['exposure','coef']))
hr_ci_low = float(np.exp(summ.loc['exposure','coef lower 95%']))
hr_ci_high = float(np.exp(summ.loc['exposure','coef upper 95%']))
p_exposure = float(summ.loc['exposure','p'])
hr_age = float(np.exp(summ.loc['age','coef']))

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
