import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import json

df = pd.read_csv('data.csv')
df = df[(df['age']>=18) & (df['age']<=80)]
df = df[df['math_score'].notna()]
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score'] - mean).abs() <= 3*sd]
df['math_score_adj'] = df['math_score'].clip(lower=1)
df['log_math'] = np.log(df['math_score_adj'])

r_all, p_all = spearmanr(df['baseline'], df['log_math'])
n_all = len(df)

tut = df[df['program']=='tutoring']
r_tut, p_tut = spearmanr(tut['baseline'], tut['log_math'])
n_tut = len(tut)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tut,
 'r_tutoring': r_tut
}
print(json.dumps(result))
