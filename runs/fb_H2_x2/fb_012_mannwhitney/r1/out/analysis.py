import pandas as pd, numpy as np, json
from scipy.stats import mannwhitneyu

df = pd.read_csv('data.csv')

# 2. drop exact duplicates keep first
df = df.drop_duplicates(keep='first')

# 3. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 4. filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 5. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# 6. drop rows with missing savings
df = df[df['savings'].notna()]

# 7. keep only coaching/waitlist
df = df[df['program'].isin(['coaching','waitlist'])]

coaching = df.loc[df['program']=='coaching','savings']
waitlist = df.loc[df['program']=='waitlist','savings']

n_coaching = len(coaching)
n_waitlist = len(waitlist)
median_coaching = coaching.median()
median_waitlist = waitlist.median()
median_diff = median_coaching - median_waitlist

u_stat, p_value = mannwhitneyu(coaching, waitlist, alternative='two-sided', method='asymptotic', use_continuity=True)

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
