import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['math_score'])
mu, sd = df['math_score'].mean(), df['math_score'].std(ddof=1)
df = df[(df['math_score'] - mu).abs() <= 3 * sd]
df = df.assign(log_outcome=np.log(df['math_score'].clip(lower=1)))
r, p = st.spearmanr(df['baseline'], df['log_outcome'])
sub = df[df['program'] == 'tutoring']
r2, p2 = st.spearmanr(sub['baseline'], sub['log_outcome'])
out = {'n_all': len(df), 'r_all': r, 'p_all': p, 'n_tutoring': len(sub), 'r_tutoring': r2}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
