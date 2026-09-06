import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# exclusion 1: age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# exclusion 2: missing glucose_fu
df = df[df['glucose_fu'].notna()]
# exclusion 3: outliers >3 sample SD from mean
mean_g = df['glucose_fu'].mean()
sd_g = df['glucose_fu'].std(ddof=1)
low_b = mean_g - 3*sd_g
high_b = mean_g + 3*sd_g
df = df[(df['glucose_fu'] >= low_b) & (df['glucose_fu'] <= high_b)]

# tertile cutpoints of baseline on analysis sample
q1 = df['baseline'].quantile(1/3)
q2 = df['baseline'].quantile(2/3)

def assign(v):
    if v <= q1:
        return 'low'
    elif v <= q2:
        return 'middle'
    else:
        return 'high'

df['group'] = df['baseline'].apply(assign)

groups = {g: df[df['group']==g]['glucose_fu'] for g in ['low','middle','high']}
n_low = len(groups['low'])
n_middle = len(groups['middle'])
n_high = len(groups['high'])
mean_low = groups['low'].mean()
mean_middle = groups['middle'].mean()
mean_high = groups['high'].mean()

f_stat, p_value = stats.f_oneway(groups['low'], groups['middle'], groups['high'])

# eta squared
grand_mean = df['glucose_fu'].mean()
ss_between = sum(len(v)*(v.mean()-grand_mean)**2 for v in groups.values())
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
