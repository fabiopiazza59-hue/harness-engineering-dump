import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# exclusion 2: missing math_score
df = df[df['math_score'].notna()]

# exclusion 3: outliers >3 sd from mean (sample sd, n-1)
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score'] >= mean-3*sd) & (df['math_score'] <= mean+3*sd)]

# transform
ms = df['math_score'].clip(lower=1)
df['log_math_score'] = np.log(ms)

# full sample
n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math_score'])

# tutoring group
dft = df[df['program']=='tutoring']
n_tutoring = len(dft)
r_tutoring, p_tutoring = stats.spearmanr(dft['baseline'], dft['log_math_score'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tutoring,
 'r_tutoring': r_tutoring
}
print(json.dumps(result))
