import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 with NaN
df = df.replace(-999, np.nan)

# age filter
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
cohens_dz = mean_change / sd_change

pct_change = (second - first) / first * 100
mean_pct_change = np.mean(pct_change)

# Wilcoxon signed-rank, discard zeros, normal approx, no continuity correction
nonzero_diff = diff[diff != 0]
stat, p = wilcoxon(nonzero_diff, zero_method='wilcox', correction=False, mode='approx')

result = {
    'n_pairs': int(n_pairs),
    'mean_first': float(mean_first),
    'mean_second': float(mean_second),
    'mean_change': float(mean_change),
    'sd_change': float(sd_change),
    'w_stat': float(stat),
    'p_value': float(p),
    'cohens_dz': float(cohens_dz),
    'mean_pct_change': float(mean_pct_change)
}
print(json.dumps(result))
