import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 3. age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# 4. normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup_days'] != 0]
# administrative censoring at 730
mask = df['followup_days'] > 730
df.loc[mask, 'followup_days'] = 730
df.loc[mask, 'event'] = 0
# exposure coding
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)

# drop missing needed columns
cols = ['followup_days','event','exposure','age']
df_model = df.dropna(subset=cols)

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df_model[cols], duration_col='followup_days', event_col='event')

summ = cph.summary
n_model = df_model.shape[0]
n_events = int(df_model['event'].sum())
median_followup = float(df_model['followup_days'].median())

hr_exposure = float(np.exp(summ.loc['exposure','coef']))
hr_ci_low = float(np.exp(summ.loc['exposure','coef'] - 1.96*summ.loc['exposure','se(coef)']))
hr_ci_high = float(np.exp(summ.loc['exposure','coef'] + 1.96*summ.loc['exposure','se(coef)']))
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
import json
print(json.dumps(result))
