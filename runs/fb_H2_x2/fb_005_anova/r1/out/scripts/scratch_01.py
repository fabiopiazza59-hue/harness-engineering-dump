import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# exclusion 2: missing rt_ms
df = df[df['rt_ms'].notna()]
# exclusion 3: outliers >3 SD from mean (sample SD ddof=1)
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low_bound = mean_rt - 3*sd_rt
high_bound = mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low_bound) & (df['rt_ms']<=high_bound)]

# tertiles of baseline
cut1 = df['baseline'].quantile(1/3)
cut2 = df['baseline'].quantile(2/3)

def assign(v):
    if v <= cut1:
        return 'low'
    elif v <= cut2:
        return 'middle'
    else:
        return 'high'

df['tertile'] = df['baseline'].apply(assign)

groups = {g: df[df['tertile']==g]['rt_ms'] for g in ['low','middle','high']}

n_low = len(groups['low'])
n_middle = len(groups['middle'])
n_high = len(groups['high'])
mean_low = groups['low'].mean()
mean_middle = groups['middle'].mean()
mean_high = groups['high'].mean()

f_stat, p_value = stats.f_oneway(groups['low'], groups['middle'], groups['high'])

grand_mean = df['rt_ms'].mean()
ss_between = sum(len(g)*(g.mean()-grand_mean)**2 for g in groups.values())
ss_total = sum((df['rt_ms']-grand_mean)**2)
eta_squared = ss_between/ss_total

result = {
 'n_low': n_low,
 'mean_low': mean_low,
 'n_middle': n_middle,
 'mean_middle': mean_middle,
 'n_high': n_high,
 'mean_high': mean_high,
 'f_stat': f_stat,
 'p_value': p_value,
 'eta_squared': eta_squared
}
print(json.dumps(result))
