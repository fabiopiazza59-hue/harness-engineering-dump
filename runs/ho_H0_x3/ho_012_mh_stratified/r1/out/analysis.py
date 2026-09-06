import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')

# remove exact duplicates
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
df = df.dropna(subset=['age'])

# normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# drop rows missing program/event/site
df = df.dropna(subset=['program','event','site'])

# keep only tutoring/standard
df = df[df['program'].isin(['tutoring','standard'])]

n_total = len(df)
n_exposed = (df['program']=='tutoring').sum()

df['exposed'] = (df['program']=='tutoring').astype(int)

# crude 2x2: exposed/unexposed x event/noevent
a = ((df['exposed']==1) & (df['event']==1)).sum()
b = ((df['exposed']==1) & (df['event']==0)).sum()
c = ((df['exposed']==0) & (df['event']==1)).sum()
d = ((df['exposed']==0) & (df['event']==0)).sum()

or_crude = (a*d)/(b*c)

# MH stratified by site
sites = sorted(df['site'].dropna().unique())
num=0.0; den=0.0
var_num=0.0
P_sum=0.0; Q_sum=0.0
R_sum=0.0; S_sum=0.0
chi2_num_sum=0.0
sum_a=0.0; sum_expected=0.0; sum_var=0.0

strat = {}
for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['exposed']==1)&(sub['event']==1)).sum()
    bi = ((sub['exposed']==1)&(sub['event']==0)).sum()
    ci = ((sub['exposed']==0)&(sub['event']==1)).sum()
    di = ((sub['exposed']==0)&(sub['event']==0)).sum()
    ni = ai+bi+ci+di
    strat[s] = (ai,bi,ci,di,ni)
    if ni==0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # variance components (Robins-Breslow-Greenland)
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    P_sum += Pi*Ri
    Q_sum += (Pi*Si + Qi*Ri)
    R_sum += Ri
    S_sum += Si
    # MH chi-square components
    row1 = ai+bi
    row0 = ci+di
    col1 = ai+ci
    col0 = bi+di
    expected_ai = row1*col1/ni
    var_ai = (row1*row0*col1*col0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_expected += expected_ai
    sum_var += var_ai

or_mh = num/den

# variance of ln(OR_mh) using Robins-Breslow-Greenland formula
var_ln_or_mh = P_sum/(2*R_sum**2) + Q_sum/(2*R_sum*S_sum) + S_sum*0  # placeholder fix below
# correct RBG formula:
var_ln_or_mh = (P_sum/(2*R_sum**2)) + (Q_sum/(2*R_sum*S_sum)) + (S_sum/(2*S_sum**2))
# Actually correct formula: Var(ln OR_MH) = sum(Pi*Ri)/(2*R^2) + sum(Pi*Si+Qi*Ri)/(2*R*S) + sum(Qi*Si)/(2*S^2)
# need Q_sum split properly; recompute with explicit sums

num=0.0; den=0.0
sumPR=0.0; sumPSQR=0.0; sumQS=0.0
R_sum=0.0; S_sum=0.0
sum_a=0.0; sum_expected=0.0; sum_var=0.0
for s in sites:
    ai,bi,ci,di,ni = strat[s]
    if ni==0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sumPR += Pi*Ri
    sumPSQR += Pi*Si + Qi*Ri
    sumQS += Qi*Si
    R_sum += Ri
    S_sum += Si
    row1 = ai+bi
    row0 = ci+di
    col1 = ai+ci
    col0 = bi+di
    expected_ai = row1*col1/ni
    var_ai = (row1*row0*col1*col0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_expected += expected_ai
    sum_var += var_ai

or_mh = num/den
var_ln_or_mh = sumPR/(2*R_sum**2) + sumPSQR/(2*R_sum*S_sum) + sumQS/(2*S_sum**2)
se_ln_or_mh = np.sqrt(var_ln_or_mh)
ln_or_mh = np.log(or_mh)
ci_low = np.exp(ln_or_mh - 1.96*se_ln_or_mh)
ci_high = np.exp(ln_or_mh + 1.96*se_ln_or_mh)

# MH chi-square with continuity correction
mh_chi2 = (abs(sum_a - sum_expected) - 0.5)**2 / sum_var
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site1 OR
ai,bi,ci,di,ni = strat[1]
or_site1 = (ai*di)/(bi*ci)

result = {
 'n_total': int(n_total),
 'n_exposed': int(n_exposed),
 'or_crude': float(or_crude),
 'or_mh': float(or_mh),
 'or_mh_ci_low': float(ci_low),
 'or_mh_ci_high': float(ci_high),
 'mh_chi2': float(mh_chi2),
 'mh_p': float(mh_p),
 'or_site1': float(or_site1)
}
import json
print(json.dumps(result))
