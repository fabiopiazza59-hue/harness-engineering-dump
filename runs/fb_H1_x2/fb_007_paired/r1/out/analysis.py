import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['math_score','math_score_post'])

n_pairs = len(df)
mean_first = df['math_score'].mean()
mean_second = df['math_score_post'].mean()
diff = df['math_score_post'] - df['math_score']
mean_change = diff.mean()
sd_change = diff.std(ddof=1)
t_stat, p_value = stats.ttest_rel(df['math_score_post'], df['math_score'])
cohens_dz = mean_change/sd_change
pct_change = diff/df['math_score']*100
mean_pct_change = pct_change.mean()

result = {
 'n_pairs': n_pairs,
 'mean_first': mean_first,
 'mean_second': mean_second,
 'mean_change': mean_change,
 'sd_change': sd_change,
 't_stat': t_stat,
 'p_value': p_value,
 'cohens_dz': cohens_dz,
 'mean_pct_change': mean_pct_change
}
print(json.dumps(result))
