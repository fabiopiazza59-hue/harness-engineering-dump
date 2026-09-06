import pandas as pd, numpy as np
from lifelines import CoxPHFitter

df = pd.read_csv('data.csv')
print('initial', df.shape)

# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
print('after dedup', df.shape)

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', df.shape)

# 4. normalize treatment
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
print(df['treatment_norm'].value_counts())

# 5. follow-up days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
print('followup stats', df['followup'].describe())

# exclude zero followup
df = df[df['followup'] > 0]
print('after excl zero followup', df.shape)

# administrative censoring at 730
df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

# exposure coding
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
print(df['exposure'].value_counts())

# complete case for model vars
model_df = df.dropna(subset=['age','event_c','followup','exposure']).copy()
print('model n', model_df.shape)

cph = CoxPHFitter()
cph.fit(model_df[['followup','event_c','exposure','age']], duration_col='followup', event_col='event_c', tie_method='breslow' if hasattr(CoxPHFitter,'tie_method') else None)
print(cph.summary)
