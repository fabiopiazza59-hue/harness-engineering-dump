import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 2. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 3. replace -999 with NaN
df = df.replace(-999, np.nan)

# 4. filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 5. normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()

# 6. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 7. censor at 730
mask_long = df['followup'] > 730
df.loc[mask_long, 'event'] = 0
df.loc[mask_long, 'followup'] = 730

# 8. exclude followup==0
df = df[df['followup'] != 0]

# 9. exposure variable
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition']=='caffeine').astype(int)

# drop missing age (already done) and missing needed cols
cols_needed = ['followup','event','exposure','age']
df = df.dropna(subset=cols_needed)

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(df[['followup','event','exposure','age']], duration_col='followup', event_col='event')

summary = cph.summary
hr_exposure = float(np.exp(summary.loc['exposure','coef']))
se_exp = summary.loc['exposure','se(coef)']
coef_exp = summary.loc['exposure','coef']
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
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
print(json.dumps(result))
