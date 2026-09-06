import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# normalise treatment
df['treatment'] = df['treatment'].str.strip().str.lower()

# exclude missing biomass
df = df.dropna(subset=['biomass'])

fert = df[df['treatment'] == 'fertilised']['biomass']
unfert = df[df['treatment'] == 'unfertilised']['biomass']

n_f = len(fert)
n_u = len(unfert)
med_f = fert.median()
med_u = unfert.median()
med_diff = med_f - med_u

res = stats.mannwhitneyu(fert, unfert, alternative='two-sided', method='asymptotic', use_continuity=True)
U = res.statistic
p = res.pvalue

rank_biserial = 1 - 2*U/(n_f*n_u)

claims = {
 'n_unfertilised': n_u,
 'n_fertilised': n_f,
 'median_unfertilised': med_u,
 'median_fertilised': med_f,
 'median_diff': med_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rank_biserial
}
print(json.dumps(claims))
