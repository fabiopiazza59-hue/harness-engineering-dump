import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['glucose_fu'].notna()]

mean_all = df['glucose_fu'].mean()
sd_all = df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mean_all).abs() <= 3*sd_all]

q1, q2 = df['baseline'].quantile([1/3, 2/3])

def grp(v):
    if v <= q1:
        return 'low'
    elif v <= q2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(grp)

low = df[df['group']=='low']['glucose_fu']
mid = df[df['group']=='middle']['glucose_fu']
high = df[df['group']=='high']['glucose_fu']

f_stat, p_value = stats.f_oneway(low, mid, high)

grand_mean = df['glucose_fu'].mean()
ss_total = ((df['glucose_fu'] - grand_mean)**2).sum()
ss_between = len(low)*(low.mean()-grand_mean)**2 + len(mid)*(mid.mean()-grand_mean)**2 + len(high)*(high.mean()-grand_mean)**2
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
