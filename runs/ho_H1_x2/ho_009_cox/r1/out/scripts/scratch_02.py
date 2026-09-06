import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['tutoring','standard'])]
df['exposure'] = (df['program_norm'] == 'tutoring').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['fup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['fup_days'] > 0]

df['event_c'] = df['event']
df.loc[df['fup_days'] > 730, 'event_c'] = 0
df['fup_days_c'] = df['fup_days'].clip(upper=730)

model_df = df.dropna(subset=['age','exposure','event_c','fup_days_c']).copy()

exog = model_df[['exposure','age']].values
status = model_df['event_c'].values
time = model_df['fup_days_c'].values

model = PHReg(time, exog, status=status, ties='breslow')
result_fit = model.fit()

coef = result_fit.params
se = result_fit.bse
pvals = result_fit.pvalues

hr_exposure = float(np.exp(coef[0]))
hr_ci_low = float(np.exp(coef[0] - 1.96*se[0]))
hr_ci_high = float(np.exp(coef[0] + 1.96*se[0]))
p_exposure = float(pvals[0])
hr_age = float(np.exp(coef[1]))

n_model = int(len(model_df))
n_events = int(model_df['event_c'].sum())
median_followup = float(model_df['fup_days_c'].median())

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
