import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# missing glucose_fu
df = df[df['glucose_fu'].notna()].copy()

mean_all = df['glucose_fu'].mean()
sd_all = df['glucose_fu'].std(ddof=1)
low_bound = mean_all - 3*sd_all
high_bound = mean_all + 3*sd_all
df = df[(df['glucose_fu']>=low_bound) & (df['glucose_fu']<=high_bound)].copy()

q1 = df['baseline'].quantile(1/3)
q2 = df['baseline'].quantile(2/3)

def grp(v):
    if v <= q1:
        return 'low'
    elif v <= q2:
        return 'middle'
    else:
        return 'high'

df['grp'] = df['baseline'].apply(grp)

low = df[df['grp']=='low']['glucose_fu']
mid = df[df['grp']=='middle']['glucose_fu']
high = df[df['grp']=='high']['glucose_fu']

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['glucose_fu'].mean()
ss_between = len(low)*(low.mean()-grand_mean)**2 + len(mid)*(mid.mean()-grand_mean)**2 + len(high)*(high.mean()-grand_mean)**2
ss_total = ((df['glucose_fu']-grand_mean)**2).sum()
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
