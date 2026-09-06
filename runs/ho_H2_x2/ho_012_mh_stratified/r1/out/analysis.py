import pandas as pd
import numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalise program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()

# keep only rows with valid program label and non-missing event/site
df = df[df['program_norm'].isin(['tutoring', 'standard'])]
df = df.dropna(subset=['event', 'site'])

df['exposed'] = (df['program_norm'] == 'tutoring').astype(int)

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude 2x2 table: exposed/unexposed by event/no event
a = int(((df.exposed==1) & (df.event==1)).sum())
b = int(((df.exposed==1) & (df.event==0)).sum())
c = int(((df.exposed==0) & (df.event==1)).sum())
d = int(((df.exposed==0) & (df.event==0)).sum())

or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df['site'].unique())
num = 0.0
den = 0.0
var_sum = 0.0
sum_a = 0.0
sum_E = 0.0
site1_or = None

# for MH variance (Robins-Breslow-Greenland)
P_sum = 0.0
Q_sum = 0.0
R_sum = 0.0
S_sum = 0.0

for s in sites:
    sub = df[df.site==s]
    ai = int(((sub.exposed==1)&(sub.event==1)).sum())
    bi = int(((sub.exposed==1)&(sub.event==0)).sum())
    ci = int(((sub.exposed==0)&(sub.event==1)).sum())
    di = int(((sub.exposed==0)&(sub.event==0)).sum())
    ni = ai+bi+ci+di
    if ni == 0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # expected count and variance for MH chi-square (standard formula)
    n1i = ai+bi  # exposed total
    n0i = ci+di  # unexposed total
    m1i = ai+ci  # event total
    m0i = bi+di  # no event total
    Ei = (n1i*m1i)/ni
    Vi = (n1i*n0i*m1i*m0i)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_E += Ei
    var_sum += Vi
    # RBG components
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    P_sum += Pi
    Q_sum += Qi
    R_sum += Ri
    S_sum += Si
    if s == 1:
        site1_or = (ai*di)/(bi*ci)

or_mh = num/den

# RBG variance of ln(OR_MH)
# Var(ln OR_MH) = sum(Pi*Ri)/(2*(sum Ri)^2) + sum(Pi*Si+Qi*Ri)/(2*sum Ri*sum Si) + sum(Qi*Si)/(2*(sum Si)^2)
sumR = 0.0
sumS = 0.0
PR = 0.0
PSQR = 0.0
QS = 0.0
for s in sites:
    sub = df[df.site==s]
    ai = int(((sub.exposed==1)&(sub.event==1)).sum())
    bi = int(((sub.exposed==1)&(sub.event==0)).sum())
    ci = int(((sub.exposed==0)&(sub.event==1)).sum())
    di = int(((sub.exposed==0)&(sub.event==0)).sum())
    ni = ai+bi+ci+di
    if ni == 0:
        continue
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sumR += Ri
    sumS += Si
    PR += Pi*Ri
    PSQR += Pi*Si + Qi*Ri
    QS += Qi*Si

var_ln_or_mh = PR/(2*sumR**2) + PSQR/(2*sumR*sumS) + QS/(2*sumS**2)
se_ln = np.sqrt(var_ln_or_mh)
ln_or_mh = np.log(or_mh)
ci_low = np.exp(ln_or_mh - 1.96*se_ln)
ci_high = np.exp(ln_or_mh + 1.96*se_ln)

# MH chi-square with continuity correction
mh_chi2 = (abs(sum_a - sum_E) - 0.5)**2 / var_sum
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

result = {
    'n_total': n_total,
    'n_exposed': n_exposed,
    'or_crude': or_crude,
    'or_mh': or_mh,
    'or_mh_ci_low': ci_low,
    'or_mh_ci_high': ci_high,
    'mh_chi2': mh_chi2,
    'mh_p': mh_p,
    'or_site1': site1_or
}

print(json.dumps(result))
