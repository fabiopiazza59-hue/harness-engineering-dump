import pandas as pd, numpy as np
from scipy.stats import wilcoxon
import json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# drop missing sbp
df = df.dropna(subset=['sbp_12w','sbp_12w_post'])

n_pairs = len(df)
first = df['sbp_12w'].values
second = df['sbp_12w_post'].values
diff = second - first

mean_first = first.mean()
mean_second = second.mean()
mean_change = diff.mean()
sd_change = diff.std(ddof=1)

# wilcoxon, discard zeros, normal approx, no continuity correction
w_stat, p_value = wilcoxon(diff, zero_method='wilcox', correction=False, mode='approx')

cohens_dz = mean_change / sd_change

pct_change = (second - first) / first * 100
mean_pct_change = pct_change.mean()

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
