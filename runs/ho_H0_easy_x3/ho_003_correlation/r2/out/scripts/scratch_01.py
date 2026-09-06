import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# exclude age outside 18-80
df = df[(df['age']>=18) & (df['age']<=80)]
# exclude missing math_score
df = df[df['math_score'].notna()]
# outlier removal based on sample SD (n-1)
mean = df['math_score'].mean()
sd = df['math_score'].std(ddof=1)
df = df[(df['math_score'] >= mean - 3*sd) & (df['math_score'] <= mean + 3*sd)]
# transform
ms = df['math_score'].clip(lower=1)
df['log_math'] = np.log(ms)

n_all = len(df)
r_all, p_all = stats.spearmanr(df['baseline'], df['log_math'])

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
