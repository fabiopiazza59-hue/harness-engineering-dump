import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# exclusion 1: age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# exclusion 2: missing math_score
df = df[df['math_score'].notna()]
# outlier removal: >3 sample SD from mean
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
low, high = mean-3*sd, mean+3*sd
df = df[(df['math_score']>=low) & (df['math_score']<=high)]
# transform
df = df.copy()
df['math_score_adj'] = df['math_score'].clip(lower=1)
df['log_math'] = np.log(df['math_score_adj'])

# full sample
n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math'])

# tutoring group
df_tut = df[df['program']=='tutoring']
n_tutoring = len(df_tut)
r_tutoring, p_tutoring = stats.spearmanr(df_tut['baseline'], df_tut['log_math'])

result = {
 'n_all': n_all,
 'r_all': r_all,
 'p_all': p_all,
 'n_tutoring': n_tutoring,
 'r_tutoring': r_tutoring
}
print(json.dumps(result))
