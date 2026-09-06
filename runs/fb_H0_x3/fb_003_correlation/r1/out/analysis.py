import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18)&(df['age']<=80)]
df = df[df['rt_ms'].notna()]

mean = df['rt_ms'].mean()
sd = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] >= mean-3*sd) & (df['rt_ms'] <= mean+3*sd)]

df = df.copy()
df['rt_ms_clip'] = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(df['rt_ms_clip'])

n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_rt'])

caf = df[df['condition']=='caffeine']
n_caffeine = len(caf)
r_caffeine, p_caffeine = stats.spearmanr(caf['baseline'], caf['log_rt'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_caffeine': n_caffeine,
 'r_caffeine': r_caffeine
}
print(json.dumps(result))
