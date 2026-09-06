import pandas as pd
import numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['age'])
# normalize treatment
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
df = df[df['treatment_norm'].isin(['fertilised','unfertilised'])]
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
# dates
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# exclude zero followup
df = df[df['followup_days'] > 0]
# event must be present
df = df.dropna(subset=['event'])
# administrative censoring at 730
df['event_cens'] = df['event']
df.loc[df['followup_days']>730, 'event_cens'] = 0
df['followup_cens'] = df['followup_days'].clip(upper=730)

# drop missing needed columns
model_df = df.dropna(subset=['followup_cens','event_cens','exposure','age'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup_cens','event_cens','exposure','age']], duration_col='followup_cens', event_col='event_cens')

summary = cph.summary
hr_exp = np.exp(summary.loc['exposure','coef'])
se_exp = summary.loc['exposure','se(coef)']
ci_low = np.exp(summary.loc['exposure','coef'] - 1.96*se_exp)
ci_high = np.exp(summary.loc['exposure','coef'] + 1.96*se_exp)
p_exp = summary.loc['exposure','p']
hr_age = np.exp(summary.loc['age','coef'])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_cens'].sum()),
 'median_followup_days': float(model_df['followup_cens'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(result)
