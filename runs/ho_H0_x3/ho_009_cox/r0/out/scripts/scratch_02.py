import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] != 0]
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df['followup_days'] = df['followup_days'].clip(upper=730)

model_df = df.dropna(subset=['age','exposure','followup_days','event_c']).copy()

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup_days'].values, exog, status=model_df['event_c'].values, ties='breslow')
result = model.fit()
print(result.summary())

coef = result.params
se = result.bse
hr_exp = np.exp(coef[0])
ci_low = np.exp(coef[0]-1.96*se[0])
ci_high = np.exp(coef[0]+1.96*se[0])
p_exp = result.pvalues[0]
hr_age = np.exp(coef[1])

import json
res = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event_c'].sum()),
 'median_followup_days': float(model_df['followup_days'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(res))
