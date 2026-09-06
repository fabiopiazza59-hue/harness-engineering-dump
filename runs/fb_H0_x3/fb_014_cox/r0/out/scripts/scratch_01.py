import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
print('initial', len(df))

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
print('after dedup', len(df))

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', len(df))

# normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
print(df['condition'].value_counts())

# compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

print(df['followup_days'].describe())

# exclude zero followup
df = df[df['followup_days'] != 0]
print('after zero followup exclusion', len(df))

# censor at 730
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df.loc[df['followup_days']>730, 'followup_days'] = 730

# exposure coding
df = df[df['condition'].isin(['placebo','caffeine'])]
df['exposure'] = (df['condition']=='caffeine').astype(int)
print('after condition filter', len(df))

# drop missing age (should be none) and other needed vars
df = df.dropna(subset=['age','exposure','followup_days','event_c'])
print('final n', len(df))

cph = CoxPHFitter(baseline_estimation_method='breslow')
model_df = df[['followup_days','event_c','exposure','age']]
cph.fit(model_df, duration_col='followup_days', event_col='event_c')
print(cph.summary)

summ = cph.summary
hr_exp = np.exp(summ.loc['exposure','coef'])
se_exp = summ.loc['exposure','se(coef)']
coef_exp = summ.loc['exposure','coef']
ci_low = np.exp(coef_exp - 1.96*se_exp)
ci_high = np.exp(coef_exp + 1.96*se_exp)
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
 'n_model': int(len(df)),
 'n_events': int(df['event_c'].sum()),
 'median_followup_days': float(df['followup_days'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
import json
print(json.dumps(result))
