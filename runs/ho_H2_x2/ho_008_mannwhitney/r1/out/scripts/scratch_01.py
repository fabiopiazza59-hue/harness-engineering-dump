import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

# drop missing glucose_fu
df = df[df['glucose_fu'].notna()]

usual = df[df['diet_norm'] == 'usual']['glucose_fu']
med = df[df['diet_norm'] == 'mediterranean']['glucose_fu']

n_usual = len(usual)
n_med = len(med)

median_usual = usual.median()
median_med = med.median()
median_diff = median_med - median_usual

res = stats.mannwhitneyu(med, usual, alternative='two-sided', use_continuity=True, method='asymptotic')
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_med*n_usual)

claims = {
 'n_usual': n_usual,
 'n_mediterranean': n_med,
 'median_usual': median_usual,
 'median_mediterranean': median_med,
 'median_diff': median_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(claims))
