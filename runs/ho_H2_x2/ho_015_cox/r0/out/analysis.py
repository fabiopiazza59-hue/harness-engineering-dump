import pandas as pd, numpy as np
from statsmodels.duration.hazard_regression import PHReg
import json

df = pd.read_csv('data.csv')
# 2. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 3. sentinel -999 -> NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 4. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# 5. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program_norm'].isin(['coaching','waitlist'])]
df['exposure'] = (df['program_norm'] == 'coaching').astype(int)
# 6. followup days
df['enrol_date'] = pd.to_datetime(df['enrol_date'])
df['last_contact_date'] = pd.to_datetime(df['last_contact_date'])
df['followup'] = (df['last_contact_date'] - df['enrol_date']).dt.days
# 7. exclude zero followup
df = df[df['followup'] != 0]
# 8. administrative censoring at 730
over = df['followup'] > 730
df.loc[over, 'followup'] = 730
df.loc[over, 'event'] = 0
# 9. complete case on needed vars
needed = ['age','exposure','event','followup']
df = df.dropna(subset=needed)
df = df.reset_index(drop=True)

n_model = len(df)
n_events = int(df['event'].sum())
median_followup = float(df['followup'].median())

exog = df[['exposure','age']].astype(float)
model = PHReg(df['followup'].astype(float), exog, status=df['event'].astype(float), ties='breslow')
result_fit = model.fit()

params = result_fit.params
se = result_fit.bse
names = list(exog.columns)
idx_exp = names.index('exposure')
idx_age = names.index('age')

hr_exposure = float(np.exp(params[idx_exp]))
hr_ci_low = float(np.exp(params[idx_exp] - 1.96*se[idx_exp]))
hr_ci_high = float(np.exp(params[idx_exp] + 1.96*se[idx_exp]))
# p-value from Wald test
zval = params[idx_exp]/se[idx_exp]
from scipy import stats
p_exposure = float(2*(1-stats.norm.cdf(abs(zval))))
hr_age = float(np.exp(params[idx_age]))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'median_followup_days': median_followup,
 'hr_exposure': hr_exposure,
 'hr_ci_low': hr_ci_low,
 'hr_ci_high': hr_ci_high,
 'p_exposure': p_exposure,
 'hr_age': hr_age
}
print(json.dumps(result))
