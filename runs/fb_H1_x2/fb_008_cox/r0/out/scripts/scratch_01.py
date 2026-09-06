import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN in numeric columns
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols] = df[num_cols].replace(-999, np.nan)

# 3. normalize treatment
df['treatment'] = df['treatment'].astype(str).str.strip().str.lower()

# 4. filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 5. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# 6. exclude zero followup
df = df[df['followup'] != 0]

# 7. administrative censoring at 730
mask = df['followup'] > 730
df.loc[mask, 'followup'] = 730
df.loc[mask, 'event'] = 0

# 8. exposure coding
df['exposure'] = (df['treatment']=='fertilised').astype(int)

# keep only rows with valid treatment labels (fertilised/unfertilised)
df = df[df['treatment'].isin(['fertilised','unfertilised'])]

# 9. complete case for model vars
model_df = df.dropna(subset=['age','event','followup','exposure']).copy()

n_model = len(model_df)
n_events = int(model_df['event'].sum())
median_followup = float(model_df['followup'].median())

cph = CoxPHFitter(baseline_estimation_method='breslow')
cph.fit(model_df[['followup','event','exposure','age']], duration_col='followup', event_col='event')

summary = cph.summary
hr_exposure = float(np.exp(summary.loc['exposure','coef']))
hr_ci_low = float(np.exp(summary.loc['exposure','coef'] - 1.96*summary.loc['exposure','se(coef)']))
hr_ci_high = float(np.exp(summary.loc['exposure','coef'] + 1.96*summary.loc['exposure','se(coef)']))
p_exposure = float(summary.loc['exposure','p'])
hr_age = float(np.exp(summary.loc['age','coef']))

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
