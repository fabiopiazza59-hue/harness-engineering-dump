import pandas as pd, numpy as np, json
from scipy.stats import mannwhitneyu

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['treatment_norm'] = df['treatment'].str.strip().str.lower()
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
rb = 1 - 2*U/(n_fert*n_unfert)

out = {
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'median_unfertilised': med_unfert,
 'median_fertilised': med_fert,
 'median_diff': med_diff,
 'u_stat': U,
 'p_value': p,
 'rank_biserial': rb
}
print(json.dumps(out))
