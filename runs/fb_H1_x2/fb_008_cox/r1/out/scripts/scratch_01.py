import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)

# 3. filter age 18-80 inclusive, drop missing age
df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize treatment
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)

# 5. compute follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup'] != 0]

# administrative censoring at 730
df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# drop missing needed vars
needed = ['age','event_c','followup','exposure']
df = df.dropna(subset=needed)

print(json.dumps({'n_rows': len(df), 'treatment_vals': df['treatment_norm'].unique().tolist()}))
