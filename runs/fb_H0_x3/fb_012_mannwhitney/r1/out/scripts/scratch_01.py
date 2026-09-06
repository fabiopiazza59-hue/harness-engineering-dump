import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')

# drop exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# drop missing savings
df = df.dropna(subset=['savings'])

coaching = df[df['program']=='coaching']['savings']
waitlist = df[df['program']=='waitlist']['savings']

n_coaching = len(coaching)
n_waitlist = len(waitlist)
median_coaching = float(coaching.median())
median_waitlist = float(waitlist.median())
median_diff = median_coaching - median_waitlist

res = stats.mannwhitneyu(coaching, waitlist, alternative='two-sided', use_continuity=True, method='asymptotic')
u_stat = float(res.statistic)
p_value = float(res.pvalue)
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
