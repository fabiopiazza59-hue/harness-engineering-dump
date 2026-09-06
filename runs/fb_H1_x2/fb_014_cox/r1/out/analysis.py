import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

mask_long = df['followup'] > 730
df.loc[mask_long, 'event'] = 0
df.loc[mask_long, 'followup'] = 730

df = df[df['followup'] != 0]

df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition']=='caffeine').astype(int)

cols_needed = ['followup','event','exposure','age']
df = df.dropna(subset=cols_needed)

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

exog = df[['exposure','age']]
model = PHReg(df['followup'], exog, status=df['event'], ties='breslow')
result = model.fit()

params = result.params
cov = result.cov_params()
se = np.sqrt(np.diag(cov))

coef_exp = params[0]
se_exp = se[0]
coef_age = params[1]

hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
z = coef_exp/se_exp
from scipy import stats
p_exposure = float(2*(1-stats.norm.cdf(abs(z))))
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
print(json.dumps(out))
