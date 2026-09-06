import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# exclusion 1: age 18-80
df = df[(df['age']>=18) & (df['age']<=80)]

# exclusion 2: missing rt_ms or bmi
df = df.dropna(subset=['rt_ms','bmi'])

# exclusion 3: outliers >3 SD from mean of rt_ms (sample SD, computed on this sample)
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
mask = (df['rt_ms'] - mean_rt).abs() <= 3*sd_rt
df = df[mask]

# transform
rt = df['rt_ms'].copy()
rt[rt<1] = 1
df['log_rt'] = np.log(rt)

# exposure coding
df['exposure'] = (df['condition']=='caffeine').astype(int)

# standardize continuous covariates
for col in ['age','bmi','baseline']:
    m = df[col].mean()
    s = df[col].std(ddof=1)
    df[col+'_z'] = (df[col]-m)/s

X = df[['exposure','age_z','bmi_z','baseline_z']]
X = sm.add_constant(X)
y = df['log_rt']

model = sm.OLS(y, X).fit()

result = {
 'n_model': int(model.nobs),
 'coef_exposure': float(model.params['exposure']),
 'se_exposure': float(model.bse['exposure']),
 'p_exposure': float(model.pvalues['exposure']),
 'coef_age': float(model.params['age_z']),
 'r_squared': float(model.rsquared),
 'adj_r_squared': float(model.rsquared_adj)
}
print(json.dumps(result))
