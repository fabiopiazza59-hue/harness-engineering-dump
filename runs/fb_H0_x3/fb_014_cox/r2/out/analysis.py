import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN in numeric columns
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols] = df[num_cols].replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()

# 5. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. administrative censoring at 730
df['event_c'] = df['event']
df.loc[df['followup_days']>730, 'event_c'] = 0
df.loc[df['followup_days']>730, 'followup_days'] = 730

# 7. exclude zero follow-up
df = df[df['followup_days']>0]

# 8. exposure coding
df = df[df['condition'].isin(['placebo','caffeine'])]
df['exposure'] = (df['condition']=='caffeine').astype(int)

# drop missing needed values
df = df.dropna(subset=['age','exposure','followup_days','event_c'])

model_df = df[['followup_days','event_c','exposure','age']].copy()

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup_days'], exog, status=model_df['event_c'], ties='breslow')
res = model.fit()

params = res.params
se = res.bse
coef_exp = params[0]
coef_age = params[1]
se_exp = se[0]
se_age = se[1]

hr_exp = np.exp(coef_exp)
ci_low = np.exp(coef_exp - 1.96*se_exp)
ci_high = np.exp(coef_exp + 1.96*se_exp)
from scipy.stats import norm
p_exp = 2*(1-norm.cdf(abs(coef_exp/se_exp)))
hr_age = np.exp(coef_age)

result = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event_c'].sum()),
 'median_followup_days': float(model_df['followup_days'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
