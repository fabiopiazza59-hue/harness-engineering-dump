import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# 1. age filter
df = df[(df['age']>=18)&(df['age']<=80)]

# 2. missing rt_ms, bmi
df = df.dropna(subset=['rt_ms','bmi'])

# 3. outlier removal on rt_ms >3 sd from mean
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
mask = (df['rt_ms'] - mean_rt).abs() <= 3*sd_rt
df = df[mask]

# 4. rt_ms<1 -> 1, log transform
rt = df['rt_ms'].copy()
rt[rt<1] = 1
df['log_rt'] = np.log(rt)

# 5. exposure coding
df['exposure'] = (df['condition']=='caffeine').astype(int)

# 6. standardize continuous covariates
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
 'adj_r_squared': model.rsquared_adj,
}
print(json.dumps(result))
