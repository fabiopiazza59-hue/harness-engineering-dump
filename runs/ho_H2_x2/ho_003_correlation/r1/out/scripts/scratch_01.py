import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# missing math_score
df = df[df['math_score'].notna()]

mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
low, high = mean-3*sd, mean+3*sd
df = df[(df['math_score']>=low) & (df['math_score']<=high)]

df['math_score_adj'] = df['math_score'].clip(lower=1)
df['log_math'] = np.log(df['math_score_adj'])

n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math'])

dft = df[df['program']=='tutoring']
n_tutoring = len(dft)
r_tutoring, p_tutoring = stats.spearmanr(dft['baseline'], dft['log_math'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tutoring,
 'r_tutoring': r_tutoring
}
print(json.dumps(result))
