import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df['program'] = df['program'].astype(str).str.strip().str.lower()

df = df[(df['age'] >= 18) & (df['age'] <= 80)]

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]

df['event_c'] = df['event']
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event_c'] = 0

df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program'] == 'coaching').astype(int)

needed = ['age','exposure','event_c','followup']
df = df.dropna(subset=needed)

n_model = len(df)
n_events = int(df['event_c'].sum())
median_followup = float(df['followup'].median())

X = df[['exposure','age']].values
model = PHReg(df['followup'].values, X, status=df['event_c'].values, ties='breslow')
res = model.fit()

coef_exp, coef_age = res.params
se_exp, se_age = res.bse

hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
z = coef_exp / se_exp
from scipy.stats import norm
p_exposure = float(2*(1-norm.cdf(abs(z))))
hr_age = float(np.exp(coef_age))

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
