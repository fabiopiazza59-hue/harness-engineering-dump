import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalize treatment
df['treatment'] = df['treatment'].astype(str).str.strip().str.lower()
# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup_days'] > 0]
# administrative censoring at 730
df['event_cens'] = df['event']
df.loc[df['followup_days'] > 730, 'event_cens'] = 0
df.loc[df['followup_days'] > 730, 'followup_days'] = 730
# exposure coding
df['exposure'] = (df['treatment'] == 'fertilised').astype(int)

# keep only needed columns, drop missing in covariates
model_df = df[['followup_days','event_cens','exposure','age']].dropna()

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df, duration_col='followup_days', event_col='event_cens', formula='exposure + age')

summ = cph.summary
hr_exposure = np.exp(summ.loc['exposure','coef'])
hr_ci_low = np.exp(summ.loc['exposure','coef'] - 1.96*summ.loc['exposure','se(coef)'])
hr_ci_high = np.exp(summ.loc['exposure','coef'] + 1.96*summ.loc['exposure','se(coef)'])
p_exposure = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event_cens'].sum()),
 'median_followup_days': float(model_df['followup_days'].median()),
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(hr_ci_low),
 'hr_ci_high': float(hr_ci_high),
 'p_exposure': float(p_exposure),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
