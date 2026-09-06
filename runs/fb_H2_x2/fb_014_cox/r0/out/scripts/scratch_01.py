import pandas as pd, numpy as np
from lifelines import CoxPHFitter

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

cph = CoxPHFitter(baseline_estimation_method='breslow')
model_df = df[['followup','event','exposure','age']].copy()
cph.fit(model_df, duration_col='followup', event_col='event')

summ = cph.summary
hr_exp = np.exp(summ.loc['exposure','coef'])
hr_exp_low = np.exp(summ.loc['exposure','coef'] - 1.96*summ.loc['exposure','se(coef)'])
hr_exp_high = np.exp(summ.loc['exposure','coef'] + 1.96*summ.loc['exposure','se(coef)'])
p_exp = summ.loc['exposure','p']
hr_age = np.exp(summ.loc['age','coef'])

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
import json
print(json.dumps(result))
