import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df.dropna(subset=['glucose_fu','bmi'])
df['diet_bin'] = (df['diet']=='mediterranean').astype(int)

X = df[['diet_bin','age','bmi']]
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

params = model.params
conf = model.conf_int(alpha=0.05)
pvals = model.pvalues

or_exposure = np.exp(params['diet_bin'])
or_ci_low = np.exp(conf.loc['diet_bin',0])
or_ci_high = np.exp(conf.loc['diet_bin',1])
p_exposure = pvals['diet_bin']
or_age = np.exp(params['age'])

result = {
 'n_model': int(model.nobs),
 'n_events': int(y.sum()),
 'or_exposure': float(or_exposure),
 'or_ci_low': float(or_ci_low),
 'or_ci_high': float(or_ci_high),
 'p_exposure': float(p_exposure),
 'or_age': float(or_age)
}
print(json.dumps(result))
