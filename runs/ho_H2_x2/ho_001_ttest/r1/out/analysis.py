import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['rt_ms'].notna()]

mean_all = df['rt_ms'].mean()
sd_all = df['rt_ms'].std(ddof=1)
low, high = mean_all - 3*sd_all, mean_all + 3*sd_all
df = df[(df['rt_ms']>=low) & (df['rt_ms']<=high)]

placebo = df[df['condition']=='placebo']['rt_ms']
caffeine = df[df['condition']=='caffeine']['rt_ms']

n_placebo = len(placebo)
n_caffeine = len(caffeine)
mean_placebo = placebo.mean()
mean_caffeine = caffeine.mean()
sd_placebo = placebo.std(ddof=1)
sd_caffeine = caffeine.std(ddof=1)
mean_diff = mean_caffeine - mean_placebo

t_stat, p_value = stats.ttest_ind(caffeine, placebo, equal_var=False)

pooled_sd = np.sqrt(((n_placebo-1)*sd_placebo**2 + (n_caffeine-1)*sd_caffeine**2) / (n_placebo+n_caffeine-2))
cohens_d = mean_diff / pooled_sd

result = {
 'n_placebo': n_placebo,
 'n_caffeine': n_caffeine,
 'mean_placebo': mean_placebo,
 'mean_caffeine': mean_caffeine,
 'sd_caffeine': sd_caffeine,
 'mean_diff': mean_diff,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_d': cohens_d
}
print(json.dumps(result))
