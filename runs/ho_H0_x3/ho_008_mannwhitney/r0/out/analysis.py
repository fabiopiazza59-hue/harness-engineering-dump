import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['glucose_fu'].notna()]

usual = df[df['diet_norm'] == 'usual']['glucose_fu']
med = df[df['diet_norm'] == 'mediterranean']['glucose_fu']

n_usual = len(usual)
n_med = len(med)
median_usual = usual.median()
median_med = med.median()
median_diff = median_med - median_usual

u_stat, p_value = mannwhitneyu(med, usual, alternative='two-sided', method='asymptotic', use_continuity=True)

rank_biserial = 1 - 2*u_stat/(n_med*n_usual)

result = {
 'n_usual': n_usual,
 'n_mediterranean': n_med,
 'median_usual': median_usual,
 'median_mediterranean': median_med,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}
print(json.dumps(result))
