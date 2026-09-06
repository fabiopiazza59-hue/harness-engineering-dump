import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df[df['biomass'].notna()]

grp_f = df[df['treatment']=='fertilised']
grp_u = df[df['treatment']=='unfertilised']

n_f = len(grp_f)
n_u = len(grp_u)
ev_f = grp_f['event'].sum()
ev_u = grp_u['event'].sum()
prop_f = ev_f/n_f
prop_u = ev_u/n_u
rr = prop_f/prop_u

table = [[ev_f, n_f-ev_f], [ev_u, n_u-ev_u]]
chi2, p, dof, exp = chi2_contingency(table, correction=False)

result = {
 'n_unfertilised': n_u,
 'n_fertilised': n_f,
 'events_fertilised': int(ev_f),
 'prop_unfertilised': prop_u,
 'prop_fertilised': prop_f,
 'risk_ratio': rr,
 'chi2_stat': chi2,
 'p_value': p
}
print(json.dumps(result))
