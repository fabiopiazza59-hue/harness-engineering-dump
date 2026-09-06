import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['rt_ms'])
mu, sd = df['rt_ms'].mean(), df['rt_ms'].std(ddof=1)
df = df[(df['rt_ms'] - mu).abs() <= 3 * sd]
df = df.assign(log_outcome=np.log(df['rt_ms'].clip(lower=1)))
r, p = st.spearmanr(df['baseline'], df['log_outcome'])
sub = df[df['condition'] == 'caffeine']
r2, p2 = st.spearmanr(sub['baseline'], sub['log_outcome'])
out = {'n_all': len(df), 'r_all': r, 'p_all': p, 'n_caffeine': len(sub), 'r_caffeine': r2}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
