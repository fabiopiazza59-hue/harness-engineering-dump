import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
# 2. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 3. sentinel -999 -> NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 4. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# 5. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program_norm'] == 'coaching').astype(int)
# 6. followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# 7. exclude zero followup
df = df[df['followup'] != 0]
# 8. administrative censoring at 730
over = df['followup'] > 730
df.loc[over, 'followup'] = 730
df.loc[over, 'event'] = 0
# 9. complete case on needed vars
needed = ['age','exposure','event','followup']
df = df.dropna(subset=needed)

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df[['followup','event','exposure','age']], duration_col='followup', event_col='event')

summ = cph.summary
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
print(json.dumps(result))
