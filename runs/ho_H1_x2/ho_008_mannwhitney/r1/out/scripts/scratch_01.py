import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)

# 3. age filter
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

# 5. drop missing glucose_fu
df = df[df['glucose_fu'].notna()]

# 6. keep only usual/mediterranean
df = df[df['diet_norm'].isin(['usual','mediterranean'])]

g_med = df[df['diet_norm']=='mediterranean']['glucose_fu']
g_usu = df[df['diet_norm']=='usual']['glucose_fu']

n_med = len(g_med)
n_usu = len(g_usu)
median_med = g_med.median()
median_usu = g_usu.median()
median_diff = median_med - median_usu

res = stats.mannwhitneyu(g_med, g_usu, alternative='two-sided', use_continuity=True, method='asymptotic')
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_med*n_usu)

out = {
 'n_usual': n_usu,
 'n_mediterranean': n_med,
 'median_usual': median_usu,
 'median_mediterranean': median_med,
 'median_diff': median_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(out))
