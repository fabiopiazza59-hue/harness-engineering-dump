import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
n0 = len(df)
# remove exact duplicates keep first
df = df.drop_duplicates(keep='first')
n1 = len(df)
# replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)
# filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
n2 = len(df)
# normalise treatment
df['treatment'] = df['treatment'].astype(str).str.strip().str.lower()
# drop missing biomass
df = df[df['biomass'].notna()]
n3 = len(df)

fert = df[df['treatment']=='fertilised']['biomass']
unfert = df[df['treatment']=='unfertilised']['biomass']

n_fert = len(fert)
n_unfert = len(unfert)

median_fert = fert.median()
median_unfert = unfert.median()
median_diff = median_fert - median_unfert

res = stats.mannwhitneyu(fert, unfert, alternative='two-sided', method='asymptotic', use_continuity=True)
u_stat = res.statistic
p_value = res.pvalue

rank_biserial = 1 - 2*u_stat/(n_fert*n_unfert)

print(json.dumps({
 'n0':n0,'n1':n1,'n2':n2,'n3':n3,
 'treatment_vals': df['treatment'].unique().tolist(),
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'median_unfertilised': median_unfert,
 'median_fertilised': median_fert,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}))
