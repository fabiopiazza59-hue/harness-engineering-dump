import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['program'] = df['program'].str.strip().str.lower()
t0 = pd.to_datetime(df['enrol_date']); t1 = pd.to_datetime(df['last_contact_date'])
tm = (t1 - t0).dt.days.astype(float); ev = df['event'].astype(int)
ev = np.where(tm > 730, 0, ev); tm = np.minimum(tm, 730)
df = df.assign(time=tm, ev=ev, exposure=(df['program'] == 'tutoring').astype(float)); df = df[df['time'] > 0]
m = sm.PHReg(df['time'], df[['exposure', 'age']], status=df['ev'], ties='breslow').fit()
ci = np.exp(m.params[0] + np.array([-1, 1]) * 1.959963984540054 * m.bse[0])
out = {'n_model': int(len(df)), 'n_events': int(df['ev'].sum()), 'median_followup_days': float(df['time'].median()), 'hr_exposure': float(np.exp(m.params[0])), 'hr_ci_low': float(ci[0]), 'hr_ci_high': float(ci[1]), 'p_exposure': float(m.pvalues[0]), 'hr_age': float(np.exp(m.params[1]))}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
