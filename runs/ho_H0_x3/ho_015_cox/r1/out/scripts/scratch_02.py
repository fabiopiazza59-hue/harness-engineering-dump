import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
print('initial', len(df))

df = df.drop_duplicates(keep='first')
print('after dedup', len(df))

df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', len(df))

df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
print(df['program_norm'].value_counts())
df['exposure'] = (df['program_norm']=='coaching').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]
print('after zero followup exclusion', len(df))

df['event_cens'] = df['event']
df.loc[df['followup']>730, 'event_cens'] = 0
df.loc[df['followup']>730, 'followup'] = 730

df_model = df.dropna(subset=['age','exposure','followup','event_cens'])
print('final model n', len(df_model))

X = df_model[['exposure','age']].astype(float)
model = PHReg(df_model['followup'].astype(float), X, status=df_model['event_cens'].astype(float), ties='breslow')
result = model.fit()
print(result.summary())

params = result.params
se = result.bse
coef_exp = params[0]
se_exp = se[0]
coef_age = params[1]
se_age = se[1]

n_model = len(df_model)
n_events = int(df_model['event_cens'].sum())
median_followup = float(df_model['followup'].median())

hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
z = coef_exp/se_exp
from scipy.stats import norm
p_exposure = float(2*(1-norm.cdf(abs(z))))
hr_age = float(np.exp(coef_age))

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
import json
print(json.dumps(out))
