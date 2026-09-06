import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
# dates
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup_days'] != 0]
# administrative censoring at 730
df['event_capped'] = df['event']
df.loc[df['followup_days'] > 730, 'event_capped'] = 0
df['followup_capped'] = df['followup_days'].clip(upper=730)
# exposure
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)
# drop missing age (already done) and drop rows missing needed vars
model_df = df.dropna(subset=['age','exposure','followup_capped','event_capped']).copy()

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup_capped','event_capped','exposure','age']], duration_col='followup_capped', event_col='event_capped')

summ = cph.summary
hr_exp = np.exp(summ.loc['exposure','coef'])
ci_low = np.exp(summ.loc['exposure','coef lower 95%'])
ci_high = np.exp(summ.loc['exposure','coef upper 95%'])
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_capped'].sum()),
 'median_followup_days': float(model_df['followup_capped'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
