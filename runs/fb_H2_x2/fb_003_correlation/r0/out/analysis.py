import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['rt_ms'].notna()]
mean = df['rt_ms'].mean()
sd = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] >= mean-3*sd) & (df['rt_ms'] <= mean+3*sd)]
df['rt_ms_adj'] = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(df['rt_ms_adj'])

r_all, p_all = stats.spearmanr(df['baseline'], df['log_rt'])
n_all = len(df)

caff = df[df['condition']=='caffeine']
r_caf, p_caf = stats.spearmanr(caff['baseline'], caff['log_rt'])
n_caf = len(caff)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_caffeine': n_caf,
 'r_caffeine': r_caf
}
print(json.dumps(result))
