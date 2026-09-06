import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]

df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

df = df[df['followup']>0]

model_df = df.dropna(subset=['age','exposure','followup','event_c']).copy()

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup'].values, exog, status=model_df['event_c'].values, ties='breslow')
res = model.fit()

params = res.params
se = res.bse
coef_exp = params[0]
se_exp = se[0]
coef_age = params[1]

hr_exposure = np.exp(coef_exp)
ci_low = np.exp(coef_exp - 1.96*se_exp)
ci_high = np.exp(coef_exp + 1.96*se_exp)
z = coef_exp/se_exp
from scipy import stats
p_exp = 2*(1-stats.norm.cdf(abs(z)))
hr_age = np.exp(coef_age)

n_model = len(model_df)
n_events = int(model_df['event_c'].sum())
median_fu = float(model_df['followup'].median())

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_fu,
 'hr_exposure': float(hr_exposure),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
