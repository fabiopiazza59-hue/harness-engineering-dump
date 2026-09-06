import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]

# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup'] != 0]

# administrative censoring at 730
df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df['followup_final'] = df['followup'].clip(upper=730)

# drop rows with missing needed covariates
model_df = df.dropna(subset=['age','exposure','followup_final','event_final']).copy()

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup_final','event_final','exposure','age']], duration_col='followup_final', event_col='event_final')

summ = cph.summary
hr_exp = np.exp(summ.loc['exposure','coef'])
ci_low = np.exp(summ.loc['exposure','coef'] - 1.96*summ.loc['exposure','se(coef)'])
ci_high = np.exp(summ.loc['exposure','coef'] + 1.96*summ.loc['exposure','se(coef)'])
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_final'].sum()),
 'median_followup_days': float(model_df['followup_final'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
