import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# 1. age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
# 2. missing math_score
df = df[df['math_score'].notna()]
# 3. outlier removal: >3 sample SD from overall mean of math_score
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score'] - mean).abs() <= 3*sd]

n_all = len(df)
r_all, p_all = stats.pearsonr(df['baseline'], df['math_score'])

tut = df[df['program'] == 'tutoring']
n_tutoring = len(tut)
r_tutoring, p_tutoring = stats.pearsonr(tut['baseline'], tut['math_score'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tutoring,
 'r_tutoring': r_tutoring
}
print(json.dumps(result))
