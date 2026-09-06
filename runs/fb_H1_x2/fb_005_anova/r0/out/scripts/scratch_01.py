import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18)&(df['age']<=80)]

# exclusion 2: missing rt_ms
df = df[df['rt_ms'].notna()]

# exclusion 3: outliers >3 SD from mean (sample SD, n-1)
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low_bound = mean_rt - 3*sd_rt
high_bound = mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low_bound)&(df['rt_ms']<=high_bound)]

# tertile cutpoints of baseline in analysis sample
cut1 = df['baseline'].quantile(1/3)
cut2 = df['baseline'].quantile(2/3)

def group(v):
    if v <= cut1:
        return 'low'
    elif v <= cut2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(group)

low = df[df['group']=='low']['rt_ms']
mid = df[df['group']=='middle']['rt_ms']
high = df[df['group']=='high']['rt_ms']

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['rt_ms'].mean()
ss_between = sum(len(g)*(g.mean()-grand_mean)**2 for g in [low, mid, high])
ss_total = sum((df['rt_ms']-grand_mean)**2)
eta_squared = ss_between/ss_total

result = {
    'n_low': len(low),
    'mean_low': low.mean(),
    'n_middle': len(mid),
    'mean_middle': mid.mean(),
    'n_high': len(high),
    'mean_high': high.mean(),
    'f_stat': f_stat,
    'p_value': p_value,
    'eta_squared': eta_squared
}
print(json.dumps(result))
