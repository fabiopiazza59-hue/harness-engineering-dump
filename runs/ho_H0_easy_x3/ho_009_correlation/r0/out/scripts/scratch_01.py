import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['glucose_fu'].notna()]
mean = df['glucose_fu'].mean()
sd = df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu']-mean).abs() <= 3*sd]

n_all = len(df)
r_all, p_all = stats.pearsonr(df['baseline'], df['glucose_fu'])

med = df[df['diet']=='mediterranean']
n_med = len(med)
r_med, p_med = stats.pearsonr(med['baseline'], med['glucose_fu'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_mediterranean': n_med,
 'r_mediterranean': r_med
}
print(json.dumps(result))
