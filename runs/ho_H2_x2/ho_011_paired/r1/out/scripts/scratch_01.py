import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# drop exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# drop missing sbp
df = df.dropna(subset=['sbp_12w', 'sbp_12w_post'])

n_pairs = len(df)
mean_first = df['sbp_12w'].mean()
mean_second = df['sbp_12w_post'].mean()
diff = df['sbp_12w_post'] - df['sbp_12w']
mean_change = diff.mean()
sd_change = diff.std(ddof=1)

# wilcoxon, discard zeros, normal approx, no continuity correction
nonzero = diff[diff != 0]
w_stat, p_value = stats.wilcoxon(nonzero, zero_method='wilcox', correction=False, mode='approx')

cohens_dz = mean_change / sd_change

pct_change = diff / df['sbp_12w'] * 100
mean_pct_change = pct_change.mean()

result = {
    'n_pairs': n_pairs,
    'mean_first': mean_first,
    'mean_second': mean_second,
    'mean_change': mean_change,
    'sd_change': sd_change,
    'w_stat': w_stat,
    'p_value': p_value,
    'cohens_dz': cohens_dz,
    'mean_pct_change': mean_pct_change,
}
print(json.dumps(result))
