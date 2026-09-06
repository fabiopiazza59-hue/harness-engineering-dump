import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program']=='coaching').astype(int)
# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup']>0]
# censor at 730
df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# drop missing needed columns
model_df = df.dropna(subset=['age','exposure','followup','event_c'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup','event_c','exposure','age']], duration_col='followup', event_col='event_c')

summary = cph.summary
hr_exp = np.exp(summary.loc['exposure','coef'])
ci_low = np.exp(summary.loc['exposure','coef lower 95%'])
ci_high = np.exp(summary.loc['exposure','coef upper 95%'])
p_exp = summary.loc['exposure','p']
hr_age = np.exp(summary.loc['age','coef'])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_c'].sum()),
 'median_followup_days': float(model_df['followup'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
