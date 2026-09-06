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
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] > 0]
df['event_cens'] = df['event']
df.loc[df['followup_days'] > 730, 'event_cens'] = 0
df.loc[df['followup_days'] > 730, 'followup_days'] = 730
df['exposure'] = (df['treatment'] == 'fertilised').astype(int)

model_df = df[['followup_days','event_cens','exposure','age']].dropna()

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup_days'], exog, status=model_df['event_cens'], ties='breslow')
result = model.fit()

params = result.params
cov = result.cov_params()
se = np.sqrt(np.diag(cov))

idx_exposure = 0
idx_age = 1

coef_exp = params[idx_exposure]
se_exp = se[idx_exposure]
hr_exposure = np.exp(coef_exp)
hr_ci_low = np.exp(coef_exp - 1.96*se_exp)
hr_ci_high = np.exp(coef_exp + 1.96*se_exp)

z = coef_exp/se_exp
from scipy.stats import norm
p_exposure = 2*(1-norm.cdf(abs(z)))

coef_age = params[idx_age]
hr_age = np.exp(coef_age)

out = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event_cens'].sum()),
 'median_followup_days': float(model_df['followup_days'].median()),
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(hr_ci_low),
 'hr_ci_high': float(hr_ci_high),
 'p_exposure': float(p_exposure),
 'hr_age': float(hr_age)
}
print(json.dumps(out))
