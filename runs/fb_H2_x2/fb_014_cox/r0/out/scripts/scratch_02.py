import pandas as pd, numpy as np, json
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive, drop missing age
df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalise condition
df['condition'] = df['condition'].astype(str).str.strip().str.lower()

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. censor at 730
mask_long = df['followup'] > 730
df.loc[mask_long, 'followup'] = 730
df.loc[mask_long, 'event'] = 0

# 7. exclude followup==0
df = df[df['followup'] != 0]

# 8. exposure variable
df = df[df['condition'].isin(['placebo','caffeine'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)

# 9. drop missing needed cols
df = df.dropna(subset=['age','event','followup','exposure'])

model_df = df[['followup','event','exposure','age']].copy()

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup'], exog, status=model_df['event'], ties='breslow')
res = model.fit()

params = res.params
se = res.bse
names = list(exog.columns)
idx_exp = names.index('exposure')
idx_age = names.index('age')

coef_exp = params[idx_exp]
se_exp = se[idx_exp]
hr_exp = np.exp(coef_exp)
hr_exp_low = np.exp(coef_exp - 1.96*se_exp)
hr_exp_high = np.exp(coef_exp + 1.96*se_exp)

from scipy import stats
z_exp = coef_exp/se_exp
p_exp = 2*(1-stats.norm.cdf(abs(z_exp)))

coef_age = params[idx_age]
hr_age = np.exp(coef_age)

result = {
 'n_model': int(len(model_df)),
 'n_events': int(model_df['event'].sum()),
 'median_followup_days': float(model_df['followup'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(hr_exp_low),
 'hr_ci_high': float(hr_exp_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
