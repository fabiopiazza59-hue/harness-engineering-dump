import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['biomass'].notna()]

mean_all = df['biomass'].mean()
sd_all = df['biomass'].std(ddof=1)
low, high = mean_all - 3*sd_all, mean_all + 3*sd_all
df = df[(df['biomass']>=low) & (df['biomass']<=high)]

g_un = df[df['treatment']=='unfertilised']['biomass']
g_fe = df[df['treatment']=='fertilised']['biomass']

n_un = len(g_un)
n_fe = len(g_fe)
mean_un = g_un.mean()
mean_fe = g_fe.mean()
sd_un = g_un.std(ddof=1)
sd_fe = g_fe.std(ddof=1)
mean_diff = mean_fe - mean_un

t_stat, p_value = stats.ttest_ind(g_fe, g_un, equal_var=True)

pooled_sd = np.sqrt(((n_un-1)*sd_un**2 + (n_fe-1)*sd_fe**2)/(n_un+n_fe-2))
cohens_d = mean_diff / pooled_sd

result = {
 'n_unfertilised': n_un,
 'n_fertilised': n_fe,
 'mean_unfertilised': mean_un,
 'mean_fertilised': mean_fe,
 'sd_fertilised': sd_fe,
 'mean_diff': mean_diff,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_d': cohens_d
}
print(json.dumps(result))
