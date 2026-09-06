import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['biomass'].notna()]

grp = df.groupby('treatment')
n_unfert = int((df['treatment']=='unfertilised').sum())
n_fert = int((df['treatment']=='fertilised').sum())
events_fert = int(df.loc[df['treatment']=='fertilised','event'].sum())
events_unfert = int(df.loc[df['treatment']=='unfertilised','event'].sum())
prop_unfert = events_unfert/n_unfert
prop_fert = events_fert/n_fert
risk_ratio = prop_fert/prop_unfert

table = pd.crosstab(df['treatment'], df['event'])
chi2, p, dof, exp = chi2_contingency(table, correction=False)

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
