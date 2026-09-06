import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df.dropna(subset=['biomass','bmi'])
df['treat_num'] = (df['treatment']=='fertilised').astype(int)

X = df[['treat_num','age','bmi']]
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

params = model.params
conf = model.conf_int()
pvals = model.pvalues

or_exposure = np.exp(params['treat_num'])
or_ci_low = np.exp(conf.loc['treat_num',0])
or_ci_high = np.exp(conf.loc['treat_num',1])
p_exposure = pvals['treat_num']
or_age = np.exp(params['age'])

result = {
 'n_model': int(len(df)),
 'n_events': int(df['event'].sum()),
 'or_exposure': float(or_exposure),
 'or_ci_low': float(or_ci_low),
 'or_ci_high': float(or_ci_high),
 'p_exposure': float(p_exposure),
 'or_age': float(or_age)
}
print(json.dumps(result))
