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
df.loc[df['followup_days']>730, 'followup_days'] = 730
df = df.dropna(subset=['age','event_c','exposure','followup_days'])

n_model = len(df)
n_events = int(df['event_c'].sum())
median_fu = float(df['followup_days'].median())

X = df[['exposure','age']].values
model = PHReg(df['followup_days'].values, X, status=df['event_c'].values, ties='breslow')
res = model.fit()

coef = res.params
se = res.bse
hr_exposure = float(np.exp(coef[0]))
hr_ci_low = float(np.exp(coef[0] - 1.96*se[0]))
hr_ci_high = float(np.exp(coef[0] + 1.96*se[0]))
z = coef[0]/se[0]
from scipy.stats import norm
p_exposure = float(2*(1-norm.cdf(abs(z))))
hr_age = float(np.exp(coef[1]))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_fu,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
import json
print(json.dumps(result))
