import pandas as pd, numpy as np
import statsmodels.api as sm
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program']=='coaching').astype(int)

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. exclude zero followup
df = df[df['followup_days']>0]

# 7. censor at 730
df['event_cens'] = df['event']
df.loc[df['followup_days']>730, 'event_cens'] = 0
df.loc[df['followup_days']>730, 'followup_days'] = 730

# 8. complete case on needed vars
df = df.dropna(subset=['event_cens','age','exposure','followup_days'])

n_model = len(df)
n_events = int(df['event_cens'].sum())
median_followup = float(df['followup_days'].median())

exog = df[['exposure','age']].astype(float).values
model = PHReg(df['followup_days'].values, exog, status=df['event_cens'].values, ties='breslow')
result_fit = model.fit()

params = result_fit.params
se = result_fit.bse
pvals = result_fit.pvalues

coef_exp = params[0]
se_exp = se[0]
p_exposure = float(pvals[0])
hr_exposure = float(np.exp(coef_exp))
hr_ci_low = float(np.exp(coef_exp - 1.96*se_exp))
hr_ci_high = float(np.exp(coef_exp + 1.96*se_exp))
coef_age = params[1]
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
