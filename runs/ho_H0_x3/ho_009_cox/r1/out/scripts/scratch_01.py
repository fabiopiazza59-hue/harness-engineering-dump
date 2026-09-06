import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalise program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. censor at 730
df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# 7. exclude zero followup
df = df[df['followup']>0]

# drop missing age (already filtered) and any remaining NaN in needed cols
model_df = df.dropna(subset=['age','exposure','followup','event_c']).copy()

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup','event_c','exposure','age']], duration_col='followup', event_col='event_c')

summ = cph.summary
hr_exposure = np.exp(summ.loc['exposure','coef'])
se_exp = summ.loc['exposure','se(coef)']
coef_exp = summ.loc['exposure','coef']
ci_low = np.exp(coef_exp - 1.96*se_exp)
ci_high = np.exp(coef_exp + 1.96*se_exp)
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

n_model = len(model_df)
n_events = int(model_df['event_c'].sum())
median_fu = float(model_df['followup'].median())

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_fu,
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
import json
print(json.dumps(result))
