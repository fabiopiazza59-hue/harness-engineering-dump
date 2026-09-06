import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# drop missing rt_ms
df = df[df['rt_ms'].notna()].copy()

mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
low_b = mean_rt - 3*sd_rt
high_b = mean_rt + 3*sd_rt
df = df[(df['rt_ms']>=low_b) & (df['rt_ms']<=high_b)].copy()

q1 = np.percentile(df['baseline'], 100/3)
q2 = np.percentile(df['baseline'], 200/3)

def grp(x):
    if x <= q1:
        return 'low'
    elif x <= q2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(grp)

low = df[df['group']=='low']['rt_ms']
mid = df[df['group']=='middle']['rt_ms']
high = df[df['group']=='high']['rt_ms']

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['rt_ms'].mean()
ss_between = sum(len(g)*(g.mean()-grand_mean)**2 for g in [low,mid,high])
ss_total = ((df['rt_ms']-grand_mean)**2).sum()
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
