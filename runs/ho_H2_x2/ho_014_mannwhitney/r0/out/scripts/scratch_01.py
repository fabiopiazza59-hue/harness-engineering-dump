import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# normalise treatment
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()

# exclude missing biomass
df = df[df['biomass'].notna()]

fert = df[df['treatment_norm'] == 'fertilised']['biomass']
unfert = df[df['treatment_norm'] == 'unfertilised']['biomass']

n_fert = len(fert)
n_unfert = len(unfert)

med_fert = fert.median()
med_unfert = unfert.median()
med_diff = med_fert - med_unfert

res = mannwhitneyu(fert, unfert, alternative='two-sided', use_continuity=True, method='asymptotic')
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_fert*n_unfert)

result = {
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'median_unfertilised': med_unfert,
 'median_fertilised': med_fert,
 'median_diff': med_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(result))
