import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['rt_ms'].notna()]

mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low_b = mean_rt - 3*sd_rt
high_b = mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low_b) & (df['rt_ms']<=high_b)]

cut1, cut2 = df['baseline'].quantile([1/3, 2/3])

def assign(x):
    if x <= cut1:
        return 'low'
    elif x <= cut2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(assign)

groups = {g: df[df['group']==g]['rt_ms'] for g in ['low','middle','high']}

n_low = len(groups['low'])
n_middle = len(groups['middle'])
n_high = len(groups['high'])
mean_low = groups['low'].mean()
mean_middle = groups['middle'].mean()
mean_high = groups['high'].mean()

f_stat, p_value = stats.f_oneway(groups['low'], groups['middle'], groups['high'])

grand_mean = df['rt_ms'].mean()
ss_total = ((df['rt_ms']-grand_mean)**2).sum()
ss_between = sum(len(v)*(v.mean()-grand_mean)**2 for v in groups.values())
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
