import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# complete case for rt_ms, bmi
df = df.dropna(subset=['rt_ms','bmi'])
# outlier removal on rt_ms
mean = df['rt_ms'].mean()
sd = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mean).abs() <= 3*sd]
# rt_ms<1 set to 1, log transform
rt = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(rt)
# exposure coding
df['exposure'] = (df['condition']=='caffeine').astype(int)
# standardize continuous covariates
for col in ['age','bmi','baseline']:
    df[col+'_std'] = (df[col]-df[col].mean())/df[col].std(ddof=1)

X = df[['exposure','age_std','bmi_std','baseline_std']]
X = sm.add_constant(X)
y = df['log_rt']
model = sm.OLS(y, X).fit()

result = {
    'n_model': int(model.nobs),
    'coef_exposure': model.params['exposure'],
    'se_exposure': model.bse['exposure'],
    'p_exposure': model.pvalues['exposure'],
    'coef_age': model.params['age_std'],
    'r_squared': model.rsquared,
    'adj_r_squared': model.rsquared_adj
}
print(json.dumps(result))
