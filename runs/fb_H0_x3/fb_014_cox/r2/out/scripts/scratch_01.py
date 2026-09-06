import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
n0 = len(df)

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

# drop missing age (should already be numeric, no -999 sentinel likely)
df = df.dropna(subset=['age','exposure','followup_days','event_c'])

cph = CoxPHFitter(baseline_estimation_method='breslow')
model_df = df[['followup_days','event_c','exposure','age']].copy()
cph.fit(model_df, duration_col='followup_days', event_col='event_c')

summary = cph.summary
hr_exp = np.exp(summary.loc['exposure','coef'])
ci_low = np.exp(summary.loc['exposure','coef'] - 1.96*summary.loc['exposure','se(coef)'])
ci_high = np.exp(summary.loc['exposure','coef'] + 1.96*summary.loc['exposure','se(coef)'])
p_exp = summary.loc['exposure','p']
hr_age = np.exp(summary.loc['age','coef'])

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
