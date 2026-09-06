import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['savings','bmi'])

df['exposure'] = (df['program']=='coaching').astype(int)

X = df[['exposure','age','bmi']].copy()
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

n_model = int(model.nobs)
n_events = int(y.sum())

params = model.params
conf = model.conf_int()
pvals = model.pvalues

or_exposure = np.exp(params['exposure'])
or_ci_low = np.exp(conf.loc['exposure',0])
or_ci_high = np.exp(conf.loc['exposure',1])
p_exposure = pvals['exposure']
or_age = np.exp(params['age'])

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
