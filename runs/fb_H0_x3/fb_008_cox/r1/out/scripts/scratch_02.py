import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['treatment_norm'] = df['treatment'].str.strip().str.lower()

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]

df['event_cens'] = df['event']
mask = df['followup']>730
df.loc[mask, 'event_cens'] = 0
df.loc[mask, 'followup'] = 730

df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)

model_df = df.dropna(subset=['age','exposure','event_cens','followup','treatment_norm'])
print('model n', len(model_df))
print('treatment values', model_df['treatment_norm'].unique())

exog = model_df[['exposure','age']]
model = PHReg(model_df['followup'], exog, status=model_df['event_cens'], ties='breslow')
result = model.fit()
print(result.summary())
print(result.params)
print(result.bse)
print(result.pvalues)
