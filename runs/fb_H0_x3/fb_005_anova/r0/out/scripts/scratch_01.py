import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['rt_ms'].notna()]

mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low_b, high_b = mean_rt-3*sd_rt, mean_rt+3*sd_rt
df = df[(df['rt_ms']>=low_b)&(df['rt_ms']<=high_b)]

cut1, cut2 = df['baseline'].quantile([1/3, 2/3])

def grp(x):
    if x <= cut1:
        return 'low'
    elif x <= cut2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(grp)

g_low = df[df['group']=='low']['rt_ms']
g_mid = df[df['group']=='middle']['rt_ms']
g_high = df[df['group']=='high']['rt_ms']

f_stat, p_value = stats.f_oneway(g_low, g_mid, g_high)

grand_mean = df['rt_ms'].mean()
ss_between = sum(len(g)*(g.mean()-grand_mean)**2 for g in [g_low,g_mid,g_high])
ss_total = ((df['rt_ms']-grand_mean)**2).sum()
eta_sq = ss_between/ss_total

result = {
 'n_low': len(g_low),
 'mean_low': g_low.mean(),
 'n_middle': len(g_mid),
 'mean_middle': g_mid.mean(),
 'n_high': len(g_high),
 'mean_high': g_high.mean(),
 'f_stat': f_stat,
 'p_value': p_value,
 'eta_squared': eta_sq
}
print(json.dumps(result))
