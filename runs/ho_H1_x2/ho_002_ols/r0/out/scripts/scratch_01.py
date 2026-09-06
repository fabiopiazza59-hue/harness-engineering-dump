import pandas as pd, numpy as np, statsmodels.api as sm, json

df = pd.read_csv('data.csv')

# age filter
df = df[(df['age']>=18)&(df['age']<=80)]

# complete case on rt_ms, bmi
df = df.dropna(subset=['rt_ms','bmi'])

# clip rt_ms below 1 to 1
df['rt_ms'] = df['rt_ms'].clip(lower=1)

# outlier removal based on rt_ms mean/sd (sample sd, n-1)
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mean_rt).abs() <= 3*sd_rt]

# log transform
df['log_rt'] = np.log(df['rt_ms'])

# exposure coding
df['exposure'] = (df['condition']=='caffeine').astype(int)

# standardize continuous covariates: age, bmi, baseline
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
  'coef_exposure': float(model.params['exposure']),
  'se_exposure': float(model.bse['exposure']),
  'p_exposure': float(model.pvalues['exposure']),
  'coef_age': float(model.params['age_std']),
  'r_squared': float(model.rsquared),
  'adj_r_squared': float(model.rsquared_adj)
}
print(json.dumps(result))
