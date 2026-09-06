import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# 3. age filter
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)
# 5. dates
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup_days'] != 0]
# administrative censoring at 730
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df['followup_days'] = df['followup_days'].clip(upper=730)

# need age, exposure, followup_days, event_c non-missing
model_df = df.dropna(subset=['age','exposure','followup_days','event_c'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup_days','event_c','exposure','age']], duration_col='followup_days', event_col='event_c')

summ = cph.summary
hr_exp = np.exp(summ.loc['exposure','coef'])
se_exp = summ.loc['exposure','se(coef)']
ci_low = np.exp(summ.loc['exposure','coef'] - 1.96*se_exp)
ci_high = np.exp(summ.loc['exposure','coef'] + 1.96*se_exp)
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event_c'].sum()),
 'median_followup_days': float(model_df['followup_days'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
import json
print(json.dumps(result))
