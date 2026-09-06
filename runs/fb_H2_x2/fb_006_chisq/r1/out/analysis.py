import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['biomass'].notna()]

fert = df[df['treatment']=='fertilised']
unfert = df[df['treatment']=='unfertilised']

n_fert = len(fert)
n_unfert = len(unfert)
events_fert = int(fert['event'].sum())
events_unfert = int(unfert['event'].sum())
prop_fert = events_fert/n_fert
prop_unfert = events_unfert/n_unfert
risk_ratio = prop_fert/prop_unfert

table = pd.crosstab(df['treatment'], df['event'])
chi2, p, dof, expected = chi2_contingency(table, correction=False)

result = {
 'n_unfertilised': n_unfert,
 'n_fertilised': n_fert,
 'events_fertilised': events_fert,
 'prop_unfertilised': prop_unfert,
 'prop_fertilised': prop_fert,
 'risk_ratio': risk_ratio,
 'chi2_stat': chi2,
 'p_value': p
}
print(json.dumps(result))
