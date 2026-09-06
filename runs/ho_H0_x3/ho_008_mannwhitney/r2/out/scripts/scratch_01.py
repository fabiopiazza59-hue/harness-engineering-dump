import pandas as pd, numpy as np
from scipy.stats import mannwhitneyu
import json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# normalize diet
df['diet'] = df['diet'].astype(str).str.strip().str.lower()
# exclude missing glucose_fu
df = df[df['glucose_fu'].notna()]

usual = df[df['diet']=='usual']['glucose_fu']
med = df[df['diet']=='mediterranean']['glucose_fu']

n_usual = len(usual)
n_med = len(med)
median_usual = usual.median()
median_med = med.median()
median_diff = median_med - median_usual

res = mannwhitneyu(med, usual, alternative='two-sided', method='asymptotic')
u_stat = res.statistic
p_value = res.pvalue
rank_biserial = 1 - 2*u_stat/(n_med*n_usual)

out = {
 'n_usual': n_usual,
 'n_mediterranean': n_med,
 'median_usual': median_usual,
 'median_mediterranean': median_med,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}
print(json.dumps(out))
