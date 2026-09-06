import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df.age>=18) & (df.age<=80)]
df = df.dropna(subset=['savings','bmi'])
df['program_bin'] = (df['program']=='coaching').astype(int)

X = df[['program_bin','age','bmi']].copy()
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

n_model = int(model.nobs)
n_events = int(y.sum())

conf = model.conf_int()
or_exposure = np.exp(model.params['program_bin'])
or_ci_low = np.exp(conf.loc['program_bin',0])
or_ci_high = np.exp(conf.loc['program_bin',1])
p_exposure = model.pvalues['program_bin']
or_age = np.exp(model.params['age'])

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
