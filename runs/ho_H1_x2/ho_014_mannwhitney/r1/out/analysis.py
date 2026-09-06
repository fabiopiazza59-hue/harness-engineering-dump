import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN (all columns, sentinel)
df = df.replace(-999, np.nan)

# 3. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalize treatment
df['treatment_norm'] = df['treatment'].str.strip().str.lower()

# 5. drop missing biomass
df = df.dropna(subset=['biomass'])

fert = df[df['treatment_norm'] == 'fertilised']['biomass']
unfert = df[df['treatment_norm'] == 'unfertilised']['biomass']

n_fert = len(fert)
n_unfert = len(unfert)
med_fert = fert.median()
med_unfert = unfert.median()
median_diff = med_fert - med_unfert

# Mann-Whitney: U for fertilised group -> x=fert, y=unfert
res = stats.mannwhitneyu(fert, unfert, alternative='two-sided', method='asymptotic', use_continuity=True)
u_stat = res.statistic
p_value = res.pvalue

rank_biserial = 1 - 2*u_stat/(n_fert*n_unfert)

result = {
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'median_unfertilised': med_unfert,
 'median_fertilised': med_fert,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}
print(json.dumps(result))
