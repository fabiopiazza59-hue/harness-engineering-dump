import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['math_score'])
mu, sd = df['math_score'].mean(), df['math_score'].std(ddof=1)
df = df[(df['math_score'] - mu).abs() <= 3 * sd]
r, p = st.pearsonr(df['baseline'], df['math_score'])
sub = df[df['program'] == 'tutoring']
r2, p2 = st.pearsonr(sub['baseline'], sub['math_score'])
out = {'n_all': len(df), 'r_all': r, 'p_all': p, 'n_tutoring': len(sub), 'r_tutoring': r2}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
