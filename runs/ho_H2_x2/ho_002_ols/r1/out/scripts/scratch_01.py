import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# exclusion: age 18-80 inclusive
df = df[(df['age']>=18)&(df['age']<=80)]

# complete case for rt_ms, bmi
df = df.dropna(subset=['rt_ms','bmi'])

# outlier removal on rt_ms >3 sd from mean
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mean_rt).abs() <= 3*sd_rt]

# transform
rt = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(rt)

# standardize covariates
for col in ['age','bmi','baseline']:
    m = df[col].mean()
    s = df[col].std(ddof=1)
    df[col+'_z'] = (df[col]-m)/s

df['exposure'] = (df['condition']=='caffeine').astype(int)

X = df[['exposure','age_z','bmi_z','baseline_z']]
X = sm.add_constant(X)
y = df['log_rt']

model = sm.OLS(y, X).fit()

result = {
 'n_model': int(model.nobs),
 'coef_exposure': model.params['exposure'],
 'se_exposure': model.bse['exposure'],
 'p_exposure': model.pvalues['exposure'],
 'coef_age': model.params['age_z'],
 'r_squared': model.rsquared,
 'adj_r_squared': model.rsquared_adj
}
print(json.dumps(result))
