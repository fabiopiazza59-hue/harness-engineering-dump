import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['biomass','bmi'])
df['nitrogen'] = (df['treatment']=='fertilised').astype(int)

X = df[['nitrogen','age','bmi']]
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

n_model = int(model.nobs)
n_events = int(y.sum())

params = model.params
conf = model.conf_int()
pvals = model.pvalues

or_exposure = np.exp(params['nitrogen'])
or_ci_low = np.exp(conf.loc['nitrogen',0])
or_ci_high = np.exp(conf.loc['nitrogen',1])
p_exposure = pvals['nitrogen']
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
