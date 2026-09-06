import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df[df['biomass'].notna()]

n_unfert = (df['treatment']=='unfertilised').sum()
n_fert = (df['treatment']=='fertilised').sum()

events_fert = df[df['treatment']=='fertilised']['event'].sum()
events_unfert = df[df['treatment']=='unfertilised']['event'].sum()

prop_fert = events_fert / n_fert
prop_unfert = events_unfert / n_unfert

risk_ratio = prop_fert / prop_unfert

ct = pd.crosstab(df['treatment'], df['event'])
chi2, p, dof, exp = chi2_contingency(ct, correction=False)

result = {
 'n_unfertilised': int(n_unfert),
 'n_fertilised': int(n_fert),
 'events_fertilised': int(events_fert),
 'prop_unfertilised': float(prop_unfert),
 'prop_fertilised': float(prop_fert),
 'risk_ratio': float(risk_ratio),
 'chi2_stat': float(chi2),
 'p_value': float(p)
}
print(json.dumps(result))
