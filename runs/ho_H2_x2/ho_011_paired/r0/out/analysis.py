import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['sbp_12w','sbp_12w_post'])

n_pairs = len(df)
first = df['sbp_12w'].values
second = df['sbp_12w_post'].values
diff = second - first
mean_first = np.mean(first)
mean_second = np.mean(second)
mean_change = np.mean(diff)
sd_change = np.std(diff, ddof=1)
cohens_dz = mean_change / sd_change
pct_change = (second-first)/first*100
mean_pct_change = np.mean(pct_change)

res = stats.wilcoxon(diff, zero_method='wilcox', correction=False, mode='approx')
w_stat = res.statistic
p_value = res.pvalue

out = {
 'n_pairs': n_pairs,
 'mean_first': mean_first,
 'mean_second': mean_second,
 'mean_change': mean_change,
 'sd_change': sd_change,
 'w_stat': w_stat,
 'p_value': p_value,
 'cohens_dz': cohens_dz,
 'mean_pct_change': mean_pct_change
}
print(json.dumps(out))
