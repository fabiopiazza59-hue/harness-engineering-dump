import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['rt_ms'].notna()]
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mean_rt).abs() <= 3*sd_rt]

cut1, cut2 = df['baseline'].quantile([1/3, 2/3])

def grp(b):
    if b <= cut1:
        return 'low'
    elif b <= cut2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(grp)

low = df[df['group']=='low']['rt_ms']
mid = df[df['group']=='middle']['rt_ms']
high = df[df['group']=='high']['rt_ms']

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['rt_ms'].mean()
ss_total = ((df['rt_ms'] - grand_mean)**2).sum()
ss_between = sum(len(g)*(g.mean()-grand_mean)**2 for g in [low, mid, high])
eta_sq = ss_between/ss_total

result = {
 'n_low': len(low),
 'mean_low': low.mean(),
 'n_middle': len(mid),
 'mean_middle': mid.mean(),
 'n_high': len(high),
 'mean_high': high.mean(),
 'f_stat': f_stat,
 'p_value': p_value,
 'eta_squared': eta_sq
}
print(json.dumps(result))
