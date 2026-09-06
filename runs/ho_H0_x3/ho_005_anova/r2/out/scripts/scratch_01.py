import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# exclude age outside 18-80
df = df[(df['age']>=18) & (df['age']<=80)]

# exclude missing glucose_fu
df = df[df['glucose_fu'].notna()]

# outlier removal: >3 sample SD from mean
mean_g = df['glucose_fu'].mean()
sd_g = df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mean_g).abs() <= 3*sd_g]

# tertile cutpoints on baseline
q1 = df['baseline'].quantile(1/3)
q2 = df['baseline'].quantile(2/3)

def grp(x):
    if x <= q1:
        return 'low'
    elif x <= q2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(grp)

low = df[df['group']=='low']['glucose_fu']
mid = df[df['group']=='middle']['glucose_fu']
high = df[df['group']=='high']['glucose_fu']

n_low, n_middle, n_high = len(low), len(mid), len(high)
mean_low, mean_middle, mean_high = low.mean(), mid.mean(), high.mean()

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['glucose_fu'].mean()
ss_between = n_low*(mean_low-grand_mean)**2 + n_middle*(mean_middle-grand_mean)**2 + n_high*(mean_high-grand_mean)**2
ss_total = ((df['glucose_fu']-grand_mean)**2).sum()
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
