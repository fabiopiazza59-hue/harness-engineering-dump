import pandas as pd, numpy as np
from lifelines import CoxPHFitter
import json

df = pd.read_csv('data.csv')
print('initial', len(df))

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
print('after dedup', len(df))

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', len(df))

# 4. normalize treatment
df['treatment_norm'] = df['treatment'].str.strip().str.lower()
print(df['treatment_norm'].value_counts())

# 5. compute followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

# exclude zero followup
df = df[df['followup'] != 0]
print('after zero followup exclusion', len(df))

# administrative censoring at 730
df['event_cens'] = df['event']
df.loc[df['followup']>730, 'event_cens'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# exposure coding
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)

# drop missing needed columns
model_df = df.dropna(subset=['age','exposure','event_cens','followup'])
print('model n', len(model_df))

cph = CoxPHFitter()
cph.fit(model_df[['followup','event_cens','exposure','age']], duration_col='followup', event_col='event_cens', ties_method='breslow' if hasattr(CoxPHFitter,'ties_method') else None)
print(cph.summary)
