import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['rt_ms'].notna()]
mean_rt = df['rt_ms'].mean()
sd_rt = df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] >= mean_rt - 3*sd_rt) & (df['rt_ms'] <= mean_rt + 3*sd_rt)]
df['rt_ms_clip'] = df['rt_ms'].clip(lower=1)
df['log_rt'] = np.log(df['rt_ms_clip'])

r_all, p_all = stats.spearmanr(df['baseline'], df['log_rt'])
n_all = len(df)

df_caf = df[df['condition']=='caffeine']
r_caf, p_caf = stats.spearmanr(df_caf['baseline'], df_caf['log_rt'])
n_caf = len(df_caf)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_caffeine': n_caf,
 'r_caffeine': r_caf
}
print(json.dumps(result))
