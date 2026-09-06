import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')

# remove exact duplicates
df = df.drop_duplicates(keep='first')

# replace -999 with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]

# normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

# dates
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup_days'] != 0]

# censor at 730
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df.loc[df['followup_days']>730, 'followup_days'] = 730

# complete case for model vars
df = df.dropna(subset=['age','event_c','exposure','followup_days'])

n_model = len(df)
n_events = int(df['event_c'].sum())
median_fu = float(df['followup_days'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df[['followup_days','event_c','exposure','age']], duration_col='followup_days', event_col='event_c')

summ = cph.summary
hr_exposure = float(np.exp(summ.loc['exposure','coef']))
se_exp = float(summ.loc['exposure','se(coef)'])
coef_exp = float(summ.loc['exposure','coef'])
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
p_exposure = float(summ.loc['exposure','p'])
hr_age = float(np.exp(summ.loc['age','coef']))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_fu,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
import json
print(json.dumps(result))
