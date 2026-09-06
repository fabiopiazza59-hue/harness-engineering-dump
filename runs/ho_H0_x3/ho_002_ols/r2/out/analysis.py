import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['rt_ms','bmi'])

mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low, high = mean_rt - 3*sd_rt, mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low) & (df['rt_ms']<=high)]

df['rt_ms_adj'] = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(df['rt_ms_adj'])

df['exposure'] = (df['condition']=='caffeine').astype(int)

for col in ['age','bmi','baseline']:
    m = df[col].mean()
    s = df[col].std(ddof=1)
    df[col+'_std'] = (df[col]-m)/s

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
    'adj_r_squared': model.rsquared_adj,
}
print(json.dumps(result))
