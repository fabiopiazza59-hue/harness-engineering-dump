import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['treatment'] = df['treatment'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup'] != 0]
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event'] = 0
df['exposure'] = np.where(df['treatment']=='fertilised', 1.0, np.where(df['treatment']=='unfertilised', 0.0, np.nan))

model_df = df.dropna(subset=['age','exposure','event','followup']).copy()

exog = model_df[['exposure','age']].values
status = model_df['event'].values
time = model_df['followup'].values

model = PHReg(time, exog, status=status, ties='breslow')
result = model.fit()

params = result.params
cov = result.cov_params()
se = np.sqrt(np.diag(cov))

hr_exposure = np.exp(params[0])
hr_ci_low = np.exp(params[0]-1.96*se[0])
hr_ci_high = np.exp(params[0]+1.96*se[0])
z = params[0]/se[0]
from scipy.stats import norm
p_exposure = 2*(1-norm.cdf(abs(z)))
hr_age = np.exp(params[1])

out = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event'].sum()),
 'median_followup_days': float(model_df['followup'].median()),
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(hr_ci_low),
 'hr_ci_high': float(hr_ci_high),
 'p_exposure': float(p_exposure),
 'hr_age': float(hr_age)
}
print(json.dumps(out))
