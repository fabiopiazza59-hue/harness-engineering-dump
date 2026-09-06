import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# exclusion 1: age between 18 and 80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# exclusion 2: drop missing savings or bmi
df = df.dropna(subset=['savings','bmi'])

df['program_bin'] = (df['program']=='coaching').astype(int)

X = df[['program_bin','age','bmi']].astype(float)
X = sm.add_constant(X)
y = df['event'].astype(float)

model = sm.Logit(y, X).fit(disp=0)

n_model = int(len(df))
n_events = int(df['event'].sum())

params = model.params
conf = model.conf_int(alpha=0.05)
pvals = model.pvalues

or_exposure = float(np.exp(params['program_bin']))
or_ci_low = float(np.exp(conf.loc['program_bin',0]))
or_ci_high = float(np.exp(conf.loc['program_bin',1]))
p_exposure = float(pvals['program_bin'])
or_age = float(np.exp(params['age']))

result = {
 'n_model': n_model,
 'n_events': n_events,
 'or_exposure': or_exposure,
 'or_ci_low': or_ci_low,
 'or_ci_high': or_ci_high,
 'p_exposure': p_exposure,
 'or_age': or_age
}
print(json.dumps(result))
