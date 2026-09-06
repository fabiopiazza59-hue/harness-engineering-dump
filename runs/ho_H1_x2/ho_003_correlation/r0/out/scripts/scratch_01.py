import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['math_score'])
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score'] >= mean-3*sd) & (df['math_score'] <= mean+3*sd)]
df['log_math'] = np.log(df['math_score'].clip(lower=1))

n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math'])

tut = df[df['program']=='tutoring']
n_tutoring = len(tut)
r_tutoring, p_tutoring = stats.spearmanr(tut['baseline'], tut['log_math'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tutoring,
 'r_tutoring': r_tutoring
}
print(json.dumps(result))
