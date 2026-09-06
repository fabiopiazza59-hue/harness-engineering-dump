import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# 3. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalize treatment
df['treatment_norm'] = df['treatment'].astype(str).str.strip().str.lower()

# 5. drop missing biomass
df = df.dropna(subset=['biomass'])

fert = df[df['treatment_norm'] == 'fertilised']['biomass']
unfert = df[df['treatment_norm'] == 'unfertilised']['biomass']

n_fert = len(fert)
n_unfert = len(unfert)

median_fert = fert.median()
median_unfert = unfert.median()
median_diff = median_fert - median_unfert

res = stats.mannwhitneyu(fert, unfert, alternative='two-sided', use_continuity=True, method='asymptotic')
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_fert*n_unfert)

claims = {
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'median_unfertilised': median_unfert,
 'median_fertilised': median_fert,
 'median_diff': median_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(claims))
