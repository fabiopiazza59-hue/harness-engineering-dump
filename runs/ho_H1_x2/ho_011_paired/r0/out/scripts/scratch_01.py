import pandas as pd, numpy as np, scipy.stats as st, json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)

# age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# drop missing sbp_12w or sbp_12w_post
df = df.dropna(subset=['sbp_12w', 'sbp_12w_post'])

n_pairs = len(df)
mean_first = df['sbp_12w'].mean()
mean_second = df['sbp_12w_post'].mean()

diff = df['sbp_12w_post'] - df['sbp_12w']
mean_change = diff.mean()
sd_change = diff.std(ddof=1)
cohens_dz = mean_change / sd_change

# Wilcoxon: discard zero differences, normal approximation, no continuity correction
diff_nonzero = diff[diff != 0]
w_stat, p_value = st.wilcoxon(diff_nonzero, zero_method='wilcox', correction=False, mode='approx')

pct_change = (df['sbp_12w_post'] - df['sbp_12w']) / df['sbp_12w'] * 100
mean_pct_change = pct_change.mean()

result = {
    'n_pairs': n_pairs,
    'mean_first': mean_first,
    'mean_second': mean_second,
    'mean_change': mean_change,
    'sd_change': sd_change,
    'w_stat': w_stat,
    'p_value': p_value,
    'cohens_dz': cohens_dz,
    'mean_pct_change': mean_pct_change
}
print(json.dumps(result))
