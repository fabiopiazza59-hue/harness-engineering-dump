import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['biomass'].notna()]

grp = df.groupby('treatment')
n_fert = (df['treatment']=='fertilised').sum()
n_unfert = (df['treatment']=='unfertilised').sum()
ev_fert = df[df['treatment']=='fertilised']['event'].sum()
ev_unfert = df[df['treatment']=='unfertilised']['event'].sum()
prop_fert = ev_fert/n_fert
prop_unfert = ev_unfert/n_unfert
risk_ratio = prop_fert/prop_unfert

table = pd.crosstab(df['treatment'], df['event'])
chi2, p, dof, exp = chi2_contingency(table, correction=False)

result = {
 'n_unfertilised': int(n_unfert),
 'n_fertilised': int(n_fert),
 'events_fertilised': int(ev_fert),
 'prop_unfertilised': prop_unfert,
 'prop_fertilised': prop_fert,
 'risk_ratio': risk_ratio,
 'chi2_stat': chi2,
 'p_value': p
}
print(json.dumps(result))
