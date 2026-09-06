import pandas as pd, numpy as np
import statsmodels.api as sm
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['standard','tutoring'])]
df['exposure'] = (df['program_norm']=='tutoring').astype(int)
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
df = df[df['followup'] != 0]
df['event_final'] = df['event']
df.loc[df['followup']>730, 'event_final'] = 0
df['followup_final'] = df['followup'].clip(upper=730)

model_df = df.dropna(subset=['age','exposure','followup_final','event_final']).copy()

exog = model_df[['exposure','age']].values
model = PHReg(model_df['followup_final'].values, exog, status=model_df['event_final'].values, ties='breslow')
res = model.fit()

coef = res.params
se = res.bse
hr_exp = np.exp(coef[0])
ci_low = np.exp(coef[0] - 1.96*se[0])
ci_high = np.exp(coef[0] + 1.96*se[0])
z = coef[0]/se[0]
from scipy import stats
p_exp = 2*(1-stats.norm.cdf(abs(z)))
hr_age = np.exp(coef[1])

result = {
 'n_model': int(model_df.shape[0]),
 'n_events': int(model_df['event_final'].sum()),
 'median_followup_days': float(model_df['followup_final'].median()),
 'hr_exposure': float(hr_exp),
 'hr_ci_low': float(ci_low),
 'hr_ci_high': float(ci_high),
 'p_exposure': float(p_exp),
 'hr_age': float(hr_age)
}
print(json.dumps(result))
