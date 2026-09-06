import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['glucose_fu'].notna()]

med = df[df['diet_norm'] == 'mediterranean']
usu = df[df['diet_norm'] == 'usual']

n_med = len(med)
n_usu = len(usu)

median_med = med['glucose_fu'].median()
median_usu = usu['glucose_fu'].median()
median_diff = median_med - median_usu

res = stats.mannwhitneyu(med['glucose_fu'], usu['glucose_fu'], alternative='two-sided', use_continuity=True, method='asymptotic')
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_med*n_usu)

result = {
 'n_usual': n_usu,
 'n_mediterranean': n_med,
 'median_usual': median_usu,
 'median_mediterranean': median_med,
 'median_diff': median_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(result))
