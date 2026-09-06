import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN everywhere
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# normalize diet
df['diet'] = df['diet'].astype(str).str.strip().str.lower()
# drop missing glucose_fu
df = df[df['glucose_fu'].notna()]

usual = df[df['diet']=='usual']['glucose_fu']
medi = df[df['diet']=='mediterranean']['glucose_fu']

n_usual = len(usual)
n_medi = len(medi)
median_usual = usual.median()
median_medi = medi.median()
median_diff = median_medi - median_usual

res = stats.mannwhitneyu(medi, usual, alternative='two-sided', method='asymptotic')
U = res.statistic
p = res.pvalue
rank_biserial = 1 - 2*U/(n_medi*n_usual)

out = {
 'n_usual': n_usual,
 'n_mediterranean': n_medi,
 'median_usual': median_usual,
 'median_mediterranean': median_medi,
 'median_diff': median_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(out))
