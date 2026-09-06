import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
print('initial', df.shape)

df = df.drop_duplicates(keep='first')
print('after dedup', df.shape)

df = df.replace(-999, np.nan)

df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', df.shape)

df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
print(df['treatment_norm'].value_counts())

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
print('followup stats', df['followup'].describe())

df = df[df['followup'] > 0]
print('after excl zero followup', df.shape)

df['event_c'] = df['event']
mask = df['followup']>730
df.loc[mask, 'event_c'] = 0
df.loc[mask, 'followup'] = 730

df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
print(df['exposure'].value_counts())

model_df = df.dropna(subset=['age','event_c','followup','exposure']).copy()
print('model n', model_df.shape)

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup'], exog, status=model_df['event_c'], ties='breslow')
result = model.fit()
print(result.summary())
print(result.params)
print(result.bse)
print(result.pvalues)
