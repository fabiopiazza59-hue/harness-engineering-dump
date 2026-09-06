import pandas as pd
import numpy as np
from statsmodels.duration.hazard_regression import PHReg

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['age'])
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()
df = df[df['treatment_norm'].isin(['fertilised','unfertilised'])]
df['exposure'] = (df['treatment_norm']=='fertilised').astype(int)
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] > 0]
df = df.dropna(subset=['event'])
df['event_cens'] = df['event']
df.loc[df['followup_days']>730, 'event_cens'] = 0
df['followup_cens'] = df['followup_days'].clip(upper=730)

model_df = df.dropna(subset=['followup_cens','event_cens','exposure','age']).copy()

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup_cens'].values, exog, status=model_df['event_cens'].values, ties='breslow')
res = model.fit()
print(res.summary())
coefs = res.params
se = res.bse
pvals = res.pvalues
hr_exp = np.exp(coefs[0])
ci_low = np.exp(coefs[0]-1.96*se[0])
ci_high = np.exp(coefs[0]+1.96*se[0])
p_exp = pvals[0]
hr_age = np.exp(coefs[1])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_cens'].sum()),
 'median_followup_days': float(model_df['followup_cens'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
import json
print(json.dumps(result))
