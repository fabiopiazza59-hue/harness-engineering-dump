import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df[df['sbp_12w'].notna()]

n_control = (df['arm']=='control').sum()
n_treatment = (df['arm']=='treatment').sum()
events_treatment = df.loc[df['arm']=='treatment', 'event'].sum()
prop_control = df.loc[df['arm']=='control', 'event'].mean()
prop_treatment = df.loc[df['arm']=='treatment', 'event'].mean()
risk_ratio = prop_treatment/prop_control

table = pd.crosstab(df['arm'], df['event'])
chi2, p, dof, expected = chi2_contingency(table, correction=False)

result = {
 'n_control': int(n_control),
 'n_treatment': int(n_treatment),
 'events_treatment': int(events_treatment),
 'prop_control': float(prop_control),
 'prop_treatment': float(prop_treatment),
 'risk_ratio': float(risk_ratio),
 'chi2_stat': float(chi2),
 'p_value': float(p)
}
print(json.dumps(result))
