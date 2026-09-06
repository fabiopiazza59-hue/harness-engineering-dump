import pandas as pd, numpy as np
from scipy.stats import chi2_contingency

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['biomass'].notna()]

g_un = df[df['treatment']=='unfertilised']
g_fe = df[df['treatment']=='fertilised']

n_un = len(g_un)
n_fe = len(g_fe)
ev_un = g_un['event'].sum()
ev_fe = g_fe['event'].sum()
prop_un = ev_un/n_un
prop_fe = ev_fe/n_fe
rr = prop_fe/prop_un

table = pd.crosstab(df['treatment'], df['event'])
chi2, p, dof, exp = chi2_contingency(table, correction=False)

result = {
 'n_unfertilised': n_un,
 'n_fertilised': n_fe,
 'events_fertilised': int(ev_fe),
 'prop_unfertilised': prop_un,
 'prop_fertilised': prop_fe,
 'risk_ratio': rr,
 'chi2_stat': chi2,
 'p_value': p
}
print(result)
