import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]

df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]

df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df.loc[df['followup']>730, 'followup'] = 730

cols_needed = ['age','exposure','event_final','followup']
df_model = df.dropna(subset=cols_needed).copy()

n_model = len(df_model)
n_events = int(df_model['event_final'].sum())
median_followup = float(df_model['followup'].median())

exog = df_model[['exposure','age']]
model = PHReg(df_model['followup'], exog, status=df_model['event_final'], ties='breslow')
result_fit = model.fit()

params = result_fit.params
bse = result_fit.bse
cov = result_fit.cov_params()

coef_exp = params[0]
coef_age = params[1]
se_exp = bse[0]

hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
z = coef_exp/se_exp
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
