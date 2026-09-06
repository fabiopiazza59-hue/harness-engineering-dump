import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age'] >= 18) & (df['age'] <= 80)]
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df.dropna(subset=['savings'])

coaching = df[df['program']=='coaching']['savings']
waitlist = df[df['program']=='waitlist']['savings']

n_coaching = len(coaching)
n_waitlist = len(waitlist)
median_coaching = coaching.median()
median_waitlist = waitlist.median()
median_diff = median_coaching - median_waitlist

res = stats.mannwhitneyu(coaching, waitlist, alternative='two-sided', use_continuity=True, method='asymptotic')
u_stat = res.statistic
p_value = res.pvalue
rank_biserial = 1 - 2*u_stat/(n_coaching*n_waitlist)

out = {
 'n_waitlist': n_waitlist,
 'n_coaching': n_coaching,
 'median_waitlist': median_waitlist,
 'median_coaching': median_coaching,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}
print(json.dumps(out))
