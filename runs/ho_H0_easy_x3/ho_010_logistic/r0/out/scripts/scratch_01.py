import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df.dropna(subset=['savings','bmi'])
df['exposure'] = (df['program']=='coaching').astype(int)

X = df[['exposure','age','bmi']].astype(float)
X = sm.add_constant(X)
y = df['event'].astype(float)

model = sm.Logit(y, X).fit(disp=0)
params = model.params
se = model.bse
conf = model.conf_int()
pvals = model.pvalues

or_exposure = np.exp(params['exposure'])
ci_low = np.exp(conf.loc['exposure',0])
ci_high = np.exp(conf.loc['exposure',1])
p_exposure = pvals['exposure']
or_age = np.exp(params['age'])

result = {
 'n_model': int(len(df)),
 'n_events': int(df['event'].sum()),
 'or_exposure': float(or_exposure),
 'or_ci_low': float(ci_low),
 'or_ci_high': float(ci_high),
 'p_exposure': float(p_exposure),
 'or_age': float(or_age)
}
print(json.dumps(result))
