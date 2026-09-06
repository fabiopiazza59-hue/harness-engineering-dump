import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
# keep only rows with known diet groups
df = df[df['diet_norm'].isin(['mediterranean','usual'])]
# drop missing event/site
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = (df['diet_norm']=='mediterranean').sum()

def make_table(sub):
    a = ((sub['diet_norm']=='mediterranean') & (sub['event']==1)).sum()
    b = ((sub['diet_norm']=='mediterranean') & (sub['event']==0)).sum()
    c = ((sub['diet_norm']=='usual') & (sub['event']==1)).sum()
    d = ((sub['diet_norm']=='usual') & (sub['event']==0)).sum()
    return a,b,c,d

a,b,c,d = make_table(df)
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num_sum = 0.0
den_sum = 0.0
chi_num_sum = 0.0
var_sum = 0.0
# for MH variance (Robins-Breslow-Day)
P_sum = 0.0
Q_sum = 0.0
R_sum = 0.0
S_sum = 0.0
sum_a = 0.0
sum_E = 0.0
sum_V = 0.0

for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = make_table(sub)
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num_sum += (ai*di)/ni
    den_sum += (bi*ci)/ni
    # MH chi-square components
    n1 = ai+bi  # exposed total
    n0 = ci+di  # unexposed total
    m1 = ai+ci  # event total
    m0 = bi+di  # nonevent total
    Ei = n1*m1/ni
    Vi = (n1*n0*m1*m0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_E += Ei
    sum_V += Vi
    # variance components for RBG CI
    P_sum += (ai+di)*(ai*di)/(ni**2)
    Q_sum += (bi+ci)*(ai*di)/(ni**2) + (ai+di)*(bi*ci)/(ni**2)
    R_sum += (bi+ci)*(bi*ci)/(ni**2)
    S_sum += 0  # placeholder

or_mh = num_sum/den_sum

# Robins-Greenland-Breslow-Day variance for ln(OR_MH)
R_num = 0.0
S_num = 0.0
Rterm = 0.0
sum_PR = 0.0
sum_PS_QR = 0.0
sum_QS = 0.0
for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = make_table(sub)
    ni = ai+bi+ci+di
    if ni==0:
        continue
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR += Pi*Si + Qi*Ri
    sum_QS += Qi*Si

var_lnOR = sum_PR/(2*num_sum**2) + sum_PS_QR/(2*num_sum*den_sum) + sum_QS/(2*den_sum**2)
se_lnOR = np.sqrt(var_lnOR)
lnOR = np.log(or_mh)
ci_low = np.exp(lnOR - 1.96*se_lnOR)
ci_high = np.exp(lnOR + 1.96*se_lnOR)

# MH chi-square with continuity correction
mh_chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_V
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site1 OR
sub1 = df[df['site']==1]
a1,b1,c1,d1 = make_table(sub1)
or_site1 = (a1*d1)/(b1*c1)

result = {
 'n_total': n_total,
 'n_exposed': int(n_exposed),
 'or_crude': or_crude,
 'or_mh': or_mh,
 'or_mh_ci_low': ci_low,
 'or_mh_ci_high': ci_high,
 'mh_chi2': mh_chi2,
 'mh_p': mh_p,
 'or_site1': or_site1
}
import json
print(json.dumps(result))
