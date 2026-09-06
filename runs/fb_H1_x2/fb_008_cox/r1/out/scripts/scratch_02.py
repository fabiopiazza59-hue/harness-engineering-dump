import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)

df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]

df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)

df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days

df = df[df['followup'] != 0]

df['event_c'] = df['event']
df.loc[df['followup']>730, 'event_c'] = 0
df.loc[df['followup']>730, 'followup'] = 730

needed = ['age','event_c','followup','exposure']
df = df.dropna(subset=needed)

X = df[['exposure','age']].values
model = PHReg(df['followup'].values, X, status=df['event_c'].values, ties='breslow')
result = model.fit()

params = result.params
se = result.bse
z = 1.96
hr = np.exp(params)
ci_low = np.exp(params - z*se)
ci_high = np.exp(params + z*se)
pvals = result.pvalues

out = {
 'n_model': int(len(df)),
 'n_events': int(df['event_c'].sum()),
 'median_followup_days': float(df['followup'].median()),
 'hr_exposure': float(hr[0]),
 'hr_ci_low': float(ci_low[0]),
 'hr_ci_high': float(ci_high[0]),
 'p_exposure': float(pvals[0]),
 'hr_age': float(hr[1])
}
print(json.dumps(out))
