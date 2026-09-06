import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')
# 2. -999 -> NaN
df = df.replace(-999, np.nan)
# 3. age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalise program
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = df['program'].map({'coaching':1,'waitlist':0})
# 5. followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup'] != 0]
# censor at 730
df.loc[df['followup']>730, 'event'] = 0
df.loc[df['followup']>730, 'followup'] = 730
# drop missing needed vars
df = df.dropna(subset=['age','exposure','event','followup'])

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

cph = CoxPHFitter()
cph.fit(df[['followup','event','exposure','age']], duration_col='followup', event_col='event', ties='breslow' if 'ties' in CoxPHFitter.fit.__code__.co_varnames else None)

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
