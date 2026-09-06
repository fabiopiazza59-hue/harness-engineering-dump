import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['condition'] = df['condition'].astype(str).str.strip().str.lower()
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup_days'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup_days'] != 0]
df['event_capped'] = df['event']
df.loc[df['followup_days'] > 730, 'event_capped'] = 0
df['followup_capped'] = df['followup_days'].clip(upper=730)
df = df[df['condition'].isin(['caffeine','placebo'])]
df['exposure'] = (df['condition'] == 'caffeine').astype(int)
model_df = df.dropna(subset=['age','exposure','followup_capped','event_capped']).copy()

X = model_df[['exposure','age']].values
model = PHReg(model_df['followup_capped'].values, X, status=model_df['event_capped'].values, ties='breslow')
res = model.fit()

coef = res.params
se = res.bse
z = 1.96
hr = np.exp(coef)
ci_low = np.exp(coef - z*se)
ci_high = np.exp(coef + z*se)
pvals = res.pvalues

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_capped'].sum()),
 'median_followup_days': float(model_df['followup_capped'].median()),
 'hr_exposure': float(hr[0]),
 'hr_ci_low': float(ci_low[0]),
 'hr_ci_high': float(ci_high[0]),
 'p_exposure': float(pvals[0]),
 'hr_age': float(hr[1])
}
print(json.dumps(result))
