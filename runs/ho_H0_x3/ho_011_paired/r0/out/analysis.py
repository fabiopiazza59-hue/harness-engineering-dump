import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicate rows
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# drop missing sbp_12w or sbp_12w_post
df = df.dropna(subset=['sbp_12w', 'sbp_12w_post'])

n_pairs = len(df)
first = df['sbp_12w'].values
second = df['sbp_12w_post'].values
diff = second - first

mean_first = np.mean(first)
mean_second = np.mean(second)
mean_change = np.mean(diff)
sd_change = np.std(diff, ddof=1)

res = stats.wilcoxon(second, first, zero_method='wilcox', correction=False, mode='approx')
w_stat = res.statistic
p_value = res.pvalue

cohens_dz = mean_change / sd_change

pct_change = (second - first) / first * 100
mean_pct_change = np.mean(pct_change)

result = {
 'n_pairs': int(n_pairs),
 'mean_first': float(mean_first),
 'mean_second': float(mean_second),
 'mean_change': float(mean_change),
 'sd_change': float(sd_change),
 'w_stat': float(w_stat),
 'p_value': float(p_value),
 'cohens_dz': float(cohens_dz),
 'mean_pct_change': float(mean_pct_change)
}
print(json.dumps(result))
