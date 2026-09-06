import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
# 3. age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()
df = df[df['program'].isin(['tutoring','standard'])]
# 5. drop missing event/site
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = (df['program']=='tutoring').sum()

def table(d):
    a = ((d['program']=='tutoring') & (d['event']==1)).sum()
    b = ((d['program']=='tutoring') & (d['event']==0)).sum()
    c = ((d['program']=='standard') & (d['event']==1)).sum()
    dd = ((d['program']=='standard') & (d['event']==0)).sum()
    return a,b,c,dd

a,b,c,dd = table(df)
or_crude = (a*dd)/(b*c)

sites = sorted(df['site'].unique())
num=0.0; den=0.0
var_sum=0.0
sum_a=0; sum_E=0
P_sum=0.0; Q_sum=0.0
R_sum=0.0; S_sum=0.0

site_tables = {}
for s in sites:
    d = df[df['site']==s]
    ai,bi,ci,di = table(d)
    ni = ai+bi+ci+di
    site_tables[s]=(ai,bi,ci,di,ni)
    if ni==0:
        continue
    num += ai*di/ni
    den += bi*ci/ni
    Ei = (ai+bi)*(ai+ci)/ni
    Vi = (ai+bi)*(ci+di)*(ai+ci)*(bi+di)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_E += Ei
    var_sum += Vi
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = ai*di/ni
    Si = bi*ci/ni
    P_sum += Pi*Ri
    Q_sum += Pi*Si + Qi*Ri
    R_sum += Qi*Si

or_mh = num/den

# RBG variance of ln(OR_mh)
R_total = num
S_total = den
var_ln_or = (P_sum/(2*R_total**2)) + (Q_sum/(2*R_total*S_total)) + (R_sum/(2*S_total**2))
se_ln_or = np.sqrt(var_ln_or)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln_or)
ci_high = np.exp(ln_or + 1.96*se_ln_or)

# MH chi-square with continuity correction
numerator = (abs(sum_a - sum_E) - 0.5)**2
mh_chi2 = numerator/var_sum
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site 1 OR
a1,b1,c1,d1,n1 = site_tables[1]
or_site1 = (a1*d1)/(b1*c1)

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
