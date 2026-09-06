import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# drop missing rt_ms or rt_ms_post
df = df.dropna(subset=['rt_ms', 'rt_ms_post'])

n_pairs = len(df)
mean_first = df['rt_ms'].mean()
mean_second = df['rt_ms_post'].mean()
diff = df['rt_ms_post'] - df['rt_ms']
mean_change = diff.mean()
sd_change = diff.std(ddof=1)
t_stat, p_value = stats.ttest_rel(df['rt_ms_post'], df['rt_ms'])
cohens_dz = mean_change / sd_change
pct_change = (df['rt_ms_post'] - df['rt_ms']) / df['rt_ms'] * 100
mean_pct_change = pct_change.mean()

result = {
 'n_pairs': n_pairs,
 'mean_first': mean_first,
 'mean_second': mean_second,
 'mean_change': mean_change,
 'sd_change': sd_change,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_dz': cohens_dz,
 'mean_pct_change': mean_pct_change
}
print(json.dumps(result))
