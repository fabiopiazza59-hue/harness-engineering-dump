import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]

df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]

df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df.loc[df['followup']>730, 'followup'] = 730

model_vars = ['followup','event_final','exposure','age']
df = df.dropna(subset=model_vars)

model = PHReg(df['followup'], df[['exposure','age']], status=df['event_final'], ties='breslow')
result = model.fit()

params = np.asarray(result.params)
bse = np.asarray(result.bse)
pvals = np.asarray(result.pvalues)

# order matches columns ['exposure','age']
hr_exposure = float(np.exp(params[0]))
se_exp = bse[0]
hr_ci_low = float(np.exp(params[0] - 1.96*se_exp))
hr_ci_high = float(np.exp(params[0] + 1.96*se_exp))
p_exposure = float(pvals[0])
hr_age = float(np.exp(params[1]))

n_model = len(df)
n_events = int(df['event_final'].sum())
median_followup = float(df['followup'].median())

out = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
print(json.dumps(out))
