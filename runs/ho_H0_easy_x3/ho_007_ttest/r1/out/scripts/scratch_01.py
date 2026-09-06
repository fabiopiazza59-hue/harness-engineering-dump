import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['biomass'].notna()]

mean_all = df['biomass'].mean()
sd_all = df['biomass'].std(ddof=1)
low, high = mean_all-3*sd_all, mean_all+3*sd_all
df = df[(df['biomass']>=low)&(df['biomass']<=high)]

unf = df[df['treatment']=='unfertilised']['biomass']
fert = df[df['treatment']=='fertilised']['biomass']

n_unf = len(unf)
n_fert = len(fert)
mean_unf = unf.mean()
mean_fert = fert.mean()
sd_unf = unf.std(ddof=1)
sd_fert = fert.std(ddof=1)
mean_diff = mean_fert - mean_unf

t_stat, p_value = stats.ttest_ind(fert, unf, equal_var=True)

pooled_sd = np.sqrt(((n_unf-1)*sd_unf**2 + (n_fert-1)*sd_fert**2)/(n_unf+n_fert-2))
cohens_d = mean_diff/pooled_sd

result = {
 'n_unfertilised': n_unf,
 'n_fertilised': n_fert,
 'mean_unfertilised': mean_unf,
 'mean_fertilised': mean_fert,
 'sd_fertilised': sd_fert,
 'mean_diff': mean_diff,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_d': cohens_d
}
print(json.dumps(result))
