import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()

# compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup_days'] != 0]

# censor at 730
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df.loc[df['followup_days']>730, 'followup_days'] = 730

# exposure coding
df = df[df['condition'].isin(['placebo','caffeine'])]
df['exposure'] = (df['condition']=='caffeine').astype(int)

# drop missing needed vars
df = df.dropna(subset=['age','exposure','followup_days','event_c'])

model = PHReg(df['followup_days'], df[['exposure','age']], status=df['event_c'], ties='breslow')
result = model.fit()

params = result.params
se = result.bse
coef_exp = params[0]
se_exp = se[0]
coef_age = params[1]

hr_exp = np.exp(coef_exp)
ci_low = np.exp(coef_exp - 1.96*se_exp)
ci_high = np.exp(coef_exp + 1.96*se_exp)
z = coef_exp/se_exp
p_exp = 2*(1-stats.norm.cdf(abs(z)))
hr_age = np.exp(coef_age)

out = {
 'n_model': int(len(df)),
 'n_events': int(df['event_c'].sum()),
 'median_followup_days': float(df['followup_days'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(out))
