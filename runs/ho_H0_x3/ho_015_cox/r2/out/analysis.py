import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = df['program'].map({'coaching':1,'waitlist':0})
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup'] != 0]
df.loc[df['followup']>730, 'event'] = 0
df.loc[df['followup']>730, 'followup'] = 730
df = df.dropna(subset=['age','exposure','event','followup'])

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

exog = df[['exposure','age']].astype(float).values
model = PHReg(df['followup'].values, exog, status=df['event'].values, ties='breslow')
res = model.fit()

coef = res.params
cov = res.cov_params()
se = np.sqrt(np.diag(cov))
z = 1.96
hr_exposure = float(np.exp(coef[0]))
hr_ci_low = float(np.exp(coef[0]-z*se[0]))
hr_ci_high = float(np.exp(coef[0]+z*se[0]))
p_exposure = float(res.pvalues[0])
hr_age = float(np.exp(coef[1]))

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
