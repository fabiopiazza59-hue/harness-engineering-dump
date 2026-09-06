import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['biomass','bmi'])
df['treat'] = (df['treatment']=='fertilised').astype(int)

X = df[['treat','age','bmi']]
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

n_model = int(len(df))
n_events = int(y.sum())

or_exposure = np.exp(model.params['treat'])
or_age = np.exp(model.params['age'])
ci = model.conf_int()
or_ci_low = np.exp(ci.loc['treat',0])
or_ci_high = np.exp(ci.loc['treat',1])
p_exposure = model.pvalues['treat']

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
