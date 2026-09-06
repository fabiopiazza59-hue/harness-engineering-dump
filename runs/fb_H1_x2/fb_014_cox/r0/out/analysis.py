import pandas as pd, numpy as np, json
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] != 0]
mask = df['followup_days'] > 730
df.loc[mask, 'followup_days'] = 730
df.loc[mask, 'event'] = 0
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)

cols = ['followup_days','event','exposure','age']
df_model = df.dropna(subset=cols).copy()

model = PHReg(df_model['followup_days'], df_model[['exposure','age']], status=df_model['event'], ties='breslow')
res = model.fit()

params = res.params
bse = res.bse
pvals = res.pvalues

n_model = int(df_model.shape[0])
n_events = int(df_model['event'].sum())
median_followup = float(df_model['followup_days'].median())

coef_exp = params[0]
se_exp = bse[0]
hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
p_exposure = float(pvals[0])
hr_age = float(np.exp(params[1]))

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
