import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
n0 = len(df)

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
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. exclude zero followup
df = df[df['followup'] != 0]

# 7. administrative censoring at 730
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event'] = 0

# 8. exposure coding
df['exposure'] = (df['treatment'] == 'fertilised').astype(float)
df.loc[~df['treatment'].isin(['fertilised','unfertilised']), 'exposure'] = np.nan

# 9. complete case for model vars
model_df = df.dropna(subset=['age','exposure','event','followup'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup','event','exposure','age']], duration_col='followup', event_col='event')

summ = cph.summary
hr_exposure = np.exp(summ.loc['exposure','coef'])
hr_ci_low = np.exp(summ.loc['exposure','coef'] - 1.96*summ.loc['exposure','se(coef)'])
hr_ci_high = np.exp(summ.loc['exposure','coef'] + 1.96*summ.loc['exposure','se(coef)'])
p_exposure = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
    'n_model': int(len(model_df)),
    'n_events': int(model_df['event'].sum()),
    'median_followup_days': float(model_df['followup'].median()),
    'hr_exposure': float(hr_exposure),
    'hr_ci_low': float(hr_ci_low),
    'hr_ci_high': float(hr_ci_high),
    'p_exposure': float(p_exposure),
    'hr_age': float(hr_age)
}
print(json.dumps(result))
