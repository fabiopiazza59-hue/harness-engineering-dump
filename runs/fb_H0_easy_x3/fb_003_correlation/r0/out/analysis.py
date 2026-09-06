import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# exclusion 2: missing rt_ms
df = df[df['rt_ms'].notna()]

# exclusion 3: outliers >3 SD from mean (sample SD, n-1)
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low, high = mean_rt - 3*sd_rt, mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low) & (df['rt_ms']<=high)]

# transform
rt_clipped = df['rt_ms'].clip(lower=1)
df = df.copy()
df['log_rt'] = np.log(rt_clipped)

# full sample correlation
r_all, p_all = stats.spearmanr(df['baseline'], df['log_rt'])
n_all = len(df)

# caffeine group
df_caf = df[df['condition']=='caffeine']
r_caf, p_caf = stats.spearmanr(df_caf['baseline'], df_caf['log_rt'])
n_caf = len(df_caf)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_caffeine': n_caf,
 'r_caffeine': r_caf
}
print(json.dumps(result))
