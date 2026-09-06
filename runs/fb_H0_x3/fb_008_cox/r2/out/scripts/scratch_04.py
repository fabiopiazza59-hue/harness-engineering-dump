import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup'] > 0]
df['event_c'] = df['event']
mask = df['followup']>730
df.loc[mask, 'event_c'] = 0
df.loc[mask, 'followup'] = 730
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
model_df = df.dropna(subset=['age','event_c','followup','exposure']).copy()

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup'], exog, status=model_df['event_c'], ties='breslow')
result = model.fit()

coef_exp = result.params[0]
se_exp = result.bse[0]
coef_age = result.params[1]

z = 1.96
hr_exposure = np.exp(coef_exp)
hr_ci_low = np.exp(coef_exp - z*se_exp)
hr_ci_high = np.exp(coef_exp + z*se_exp)
zscore = coef_exp/se_exp
p_exposure = 2*(1-stats.norm.cdf(abs(zscore)))
hr_age = np.exp(coef_age)

n_model = len(model_df)
n_events = int(model_df['event_c'].sum())
median_followup_days = float(model_df['followup'].median())

claims = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup_days,
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(hr_ci_low),
 'hr_ci_high': float(hr_ci_high),
 'p_exposure': float(p_exposure),
 'hr_age': float(hr_age)
}
print(json.dumps(claims))
