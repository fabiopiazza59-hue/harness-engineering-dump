import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
# replace -999 with NaN across all columns
df = df.replace(-999, np.nan)
# filter age 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# normalize program
df['program'] = df['program'].str.strip().str.lower()
# drop missing savings
df = df.dropna(subset=['savings'])

wait = df[df['program']=='waitlist']['savings']
coach = df[df['program']=='coaching']['savings']

n_waitlist = len(wait)
n_coaching = len(coach)
median_waitlist = wait.median()
median_coaching = coach.median()
median_diff = median_coaching - median_waitlist

u_stat, p_value = stats.mannwhitneyu(coach, wait, alternative='two-sided', method='asymptotic', use_continuity=True)
rank_biserial = 1 - 2*u_stat/(n_coaching*n_waitlist)

result = {
 'n_waitlist': n_waitlist,
 'n_coaching': n_coaching,
 'median_waitlist': median_waitlist,
 'median_coaching': median_coaching,
 'median_diff': median_diff,
 'u_stat': u_stat,
 'p_value': p_value,
 'rank_biserial': rank_biserial
}
print(json.dumps(result))
