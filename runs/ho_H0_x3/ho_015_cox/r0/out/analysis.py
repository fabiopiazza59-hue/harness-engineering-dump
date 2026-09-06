import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program']=='coaching').astype(int)
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup']>0]
df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

model_df = df.dropna(subset=['age','exposure','followup','event_c']).copy()

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup'].values, exog, status=model_df['event_c'].values, ties='breslow')
res = model.fit()

params = res.params
cov = res.cov_params()
se = np.sqrt(np.diag(cov))

hr_exp = np.exp(params[0])
ci_low = np.exp(params[0]-1.96*se[0])
ci_high = np.exp(params[0]+1.96*se[0])
z = params[0]/se[0]
from scipy.stats import norm
p_exp = 2*(1-norm.cdf(abs(z)))
hr_age = np.exp(params[1])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_c'].sum()),
 'median_followup_days': float(model_df['followup'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
