import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# 5. drop rows with missing savings
df = df.dropna(subset=['savings'])

coaching = df[df['program']=='coaching']['savings']
waitlist = df[df['program']=='waitlist']['savings']

n_coaching = len(coaching)
n_waitlist = len(waitlist)
median_coaching = float(coaching.median())
median_waitlist = float(waitlist.median())
median_diff = median_coaching - median_waitlist

u_stat, p_value = stats.mannwhitneyu(coaching, waitlist, alternative='two-sided', use_continuity=True, method='asymptotic')

rank_biserial = 1 - 2*u_stat/(n_coaching*n_waitlist)

result = {
 'n_waitlist': n_waitlist,
 'n_coaching': n_coaching,
 'median_waitlist': median_waitlist,
 'median_coaching': median_coaching,
 'median_diff': median_diff,
 'u_stat': float(u_stat),
 'p_value': float(p_value),
 'rank_biserial': float(rank_biserial)
}
print(json.dumps(result))
