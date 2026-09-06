import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['math_score'].notna()]
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score']-mean).abs() <= 3*sd]
df['log_math'] = np.log(df['math_score'].clip(lower=1))

r_all, p_all = stats.spearmanr(df['baseline'], df['log_math'])
n_all = len(df)

tut = df[df['program']=='tutoring']
r_tut, p_tut = stats.spearmanr(tut['baseline'], tut['log_math'])
n_tut = len(tut)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tut,
 'r_tutoring': r_tut
}
import json
print(json.dumps(result))
