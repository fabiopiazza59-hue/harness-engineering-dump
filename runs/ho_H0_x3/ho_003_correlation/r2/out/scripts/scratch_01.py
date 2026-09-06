import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. age filter
df = df[(df['age']>=18) & (df['age']<=80)]

# 2. missing math_score
df = df[df['math_score'].notna()]

# 3. outlier removal based on mean/std (n-1) of math_score
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
low = mean - 3*sd
high = mean + 3*sd
df = df[(df['math_score']>=low) & (df['math_score']<=high)]

# 4. log transform
df = df.copy()
df['math_score_clip'] = df['math_score'].clip(lower=1)
df['log_math_score'] = np.log(df['math_score_clip'])

# full sample correlation
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math_score'])
n_all = len(df)

# tutoring group
df_tut = df[df['program']=='tutoring']
r_tut, p_tut = stats.spearmanr(df_tut['baseline'], df_tut['log_math_score'])
n_tut = len(df_tut)

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tut,
 'r_tutoring': r_tut
}
print(json.dumps(result))
