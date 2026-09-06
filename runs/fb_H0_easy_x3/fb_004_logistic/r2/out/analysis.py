import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['glucose_fu','bmi'])
df['diet_bin'] = (df['diet']=='mediterranean').astype(int)

X = df[['diet_bin','age','bmi']]
X = sm.add_constant(X)
y = df['event']

model = sm.Logit(y, X).fit(disp=0)

n_model = int(model.nobs)
n_events = int(y.sum())

coef = model.params['diet_bin']
se = model.bse['diet_bin']
or_exposure = np.exp(coef)
ci_low = np.exp(coef - 1.96*se)
ci_high = np.exp(coef + 1.96*se)
p_exposure = model.pvalues['diet_bin']
or_age = np.exp(model.params['age'])

result = {
 'n_model': n_model,
 'n_events': n_events,
 'or_exposure': or_exposure,
 'or_ci_low': ci_low,
 'or_ci_high': ci_high,
 'p_exposure': p_exposure,
 'or_age': or_age
}
print(json.dumps(result))
