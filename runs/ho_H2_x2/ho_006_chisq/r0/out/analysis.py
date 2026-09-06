import pandas as pd
from scipy.stats import chi2_contingency
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['sbp_12w'].notna()]

ctrl = df[df['arm']=='control']
trt = df[df['arm']=='treatment']

n_control = len(ctrl)
n_treatment = len(trt)
events_treatment = trt['event'].sum()
events_control = ctrl['event'].sum()
prop_control = events_control/n_control
prop_treatment = events_treatment/n_treatment
risk_ratio = prop_treatment/prop_control

table = pd.crosstab(df['arm'], df['event'])
chi2, p, dof, exp = chi2_contingency(table, correction=False)

result = {
 'n_control': n_control,
 'n_treatment': n_treatment,
 'events_treatment': int(events_treatment),
 'prop_control': prop_control,
 'prop_treatment': prop_treatment,
 'risk_ratio': risk_ratio,
 'chi2_stat': chi2,
 'p_value': p
}
print(json.dumps(result))
