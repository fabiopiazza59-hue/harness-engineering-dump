import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['glucose_fu'])
mu, sd = df['glucose_fu'].mean(), df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mu).abs() <= 3 * sd]
r, p = st.pearsonr(df['baseline'], df['glucose_fu'])
sub = df[df['diet'] == 'mediterranean']
r2, p2 = st.pearsonr(sub['baseline'], sub['glucose_fu'])
out = {'n_all': len(df), 'r_all': r, 'p_all': p, 'n_mediterranean': len(sub), 'r_mediterranean': r2}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
