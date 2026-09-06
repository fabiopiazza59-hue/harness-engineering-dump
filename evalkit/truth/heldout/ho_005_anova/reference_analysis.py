import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
df = pd.read_csv('data.csv')
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df = df.dropna(subset=['glucose_fu'])
mu, sd = df['glucose_fu'].mean(), df['glucose_fu'].std(ddof=1)
df = df[(df['glucose_fu'] - mu).abs() <= 3 * sd]
q = df['baseline'].quantile([1/3, 2/3]).values
df = df.assign(tertile=np.where(df['baseline'] <= q[0], 'low', np.where(df['baseline'] <= q[1], 'middle', 'high')))
groups = [df.loc[df['tertile'] == k, 'glucose_fu'] for k in ('low', 'middle', 'high')]
f, p = st.f_oneway(*groups)
grand = df['glucose_fu'].mean()
ssb = sum(len(g)*(g.mean()-grand)**2 for g in groups)
sst = ((df['glucose_fu']-grand)**2).sum()
out = {'n_low': len(groups[0]), 'n_middle': len(groups[1]), 'n_high': len(groups[2]), 'mean_low': groups[0].mean(), 'mean_middle': groups[1].mean(), 'mean_high': groups[2].mean(), 'f_stat': f, 'p_value': p, 'eta_squared': ssb/sst}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
