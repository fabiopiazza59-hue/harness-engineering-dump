import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# exclusion 2: missing rt_ms
df = df[df['rt_ms'].notna()]

# exclusion 3: outliers >3 sample SD from mean
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] >= mean_rt - 3*sd_rt) & (df['rt_ms'] <= mean_rt + 3*sd_rt)]

# transform
rt_adj = df['rt_ms'].copy()
rt_adj[rt_adj < 1] = 1
df['log_rt'] = np.log(rt_adj)

# full sample correlation
n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_rt'])

# caffeine group
df_caf = df[df['condition']=='caffeine']
n_caffeine = len(df_caf)
r_caffeine, p_caffeine = stats.spearmanr(df_caf['baseline'], df_caf['log_rt'])

result = {
  'n_all': n_all,
  'r_all': r_all,
  'p_all': p_all,
  'n_caffeine': n_caffeine,
  'r_caffeine': r_caffeine
}
print(json.dumps(result))
