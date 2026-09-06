import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['glucose_fu'].notna()]
mean_all = df['glucose_fu'].mean()
sd_all = df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mean_all).abs() <= 3*sd_all]

usual = df[df['diet']=='usual']['glucose_fu']
med = df[df['diet']=='mediterranean']['glucose_fu']

n_usual = len(usual)
n_med = len(med)
mean_usual = usual.mean()
mean_med = med.mean()
sd_usual = usual.std(ddof=1)
sd_med = med.std(ddof=1)
mean_diff = mean_med - mean_usual

t_stat, p_value = stats.ttest_ind(med, usual, equal_var=True)

pooled_sd = np.sqrt(((n_usual-1)*sd_usual**2 + (n_med-1)*sd_med**2)/(n_usual+n_med-2))
cohens_d = mean_diff/pooled_sd

result = {
 'n_usual': n_usual,
 'n_mediterranean': n_med,
 'mean_usual': mean_usual,
 'mean_mediterranean': mean_med,
 'sd_mediterranean': sd_med,
 'mean_diff': mean_diff,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_d': cohens_d
}
print(json.dumps(result))
