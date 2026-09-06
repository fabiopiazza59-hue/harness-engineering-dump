import json, numpy as np, pandas as pd, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['diet'] = df['diet'].str.strip().str.lower()
df = df.assign(exposure=(df['diet'] == 'mediterranean').astype(int))
tables = [pd.crosstab(df[df['site']==s]['exposure'], df[df['site']==s]['event']).reindex(index=[1,0], columns=[1,0]).fillna(0).values for s in sorted(df['site'].unique())]
stt = sm.stats.StratifiedTable(tables); ci = stt.oddsratio_pooled_confint(alpha=0.05); test = stt.test_null_odds(correction=True)
crude = pd.crosstab(df['exposure'], df['event']).reindex(index=[1,0], columns=[1,0]).fillna(0).values
s1 = tables[0]
out = {'n_total': len(df), 'n_exposed': int(df['exposure'].sum()), 'or_crude': float((crude[0,0]*crude[1,1])/(crude[0,1]*crude[1,0])), 'or_mh': float(stt.oddsratio_pooled), 'or_mh_ci_low': float(ci[0]), 'or_mh_ci_high': float(ci[1]), 'mh_chi2': float(test.statistic), 'mh_p': float(test.pvalue), 'or_site1': float((s1[0,0]*s1[1,1])/(s1[0,1]*s1[1,0]))}
print(json.dumps({k: (int(v) if isinstance(v, (int, np.integer)) else float(v)) for k, v in out.items()}))
