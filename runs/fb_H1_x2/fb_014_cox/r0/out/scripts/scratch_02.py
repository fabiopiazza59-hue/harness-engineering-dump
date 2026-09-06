import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] != 0]
mask = df['followup_days'] > 730
df.loc[mask, 'followup_days'] = 730
df.loc[mask, 'event'] = 0
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)

cols = ['followup_days','event','exposure','age']
df_model = df.dropna(subset=cols).copy()

model = PHReg(df_model['followup_days'], df_model[['exposure','age']], status=df_model['event'], ties='breslow')
res = model.fit()
print(res.summary())
print(res.params, res.bse)
