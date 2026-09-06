import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive, drop missing age
df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()

# keep only rows with program in {tutoring, standard}
df = df[df['program_norm'].isin(['tutoring','standard'])]

# drop missing site/event
df = df[df['site'].notna() & df['event'].notna()]

n_total = len(df)
n_exposed = (df['program_norm']=='tutoring').sum()

df['exposed'] = (df['program_norm']=='tutoring').astype(int)

# crude OR
a = ((df['exposed']==1) & (df['event']==1)).sum()
b = ((df['exposed']==1) & (df['event']==0)).sum()
c = ((df['exposed']==0) & (df['event']==1)).sum()
d = ((df['exposed']==0) & (df['event']==0)).sum()
or_crude = (a*d)/(b*c)

# MH across sites
sites = sorted(df['site'].unique())
num = 0.0
den = 0.0
# for variance (Robins-Breslow-Greenland)
sum_PR = 0.0
sum_PS_QR = 0.0
sum_QS = 0.0

# for chi2 continuity corrected
sum_a = 0.0
sum_Ea = 0.0
sum_Var = 0.0

for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['exposed']==1) & (sub['event']==1)).sum()
    bi = ((sub['exposed']==1) & (sub['event']==0)).sum()
    ci = ((sub['exposed']==0) & (sub['event']==1)).sum()
    di = ((sub['exposed']==0) & (sub['event']==0)).sum()
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # RBG variance components
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR += (Pi*Si + Qi*Ri)
    sum_QS += Qi*Si
    # MH chi2
    n1i = ai+bi
    n0i = ci+di
    m1i = ai+ci
    m0i = bi+di
    Eai = n1i*m1i/ni
    Vari = (n1i*n0i*m1i*m0i)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Eai
    sum_Var += Vari

or_mh = num/den

R = num
S = den
var_lnor = sum_PR/(2*R**2) + sum_PS_QR/(2*R*S) + sum_QS/(2*S**2)
se_lnor = np.sqrt(var_lnor)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_lnor)
ci_high = np.exp(ln_or + 1.96*se_lnor)

mh_chi2 = (abs(sum_a - sum_Ea) - 0.5)**2 / sum_Var
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site 1 OR
sub1 = df[df['site']==1]
a1 = ((sub1['exposed']==1) & (sub1['event']==1)).sum()
b1 = ((sub1['exposed']==1) & (sub1['event']==0)).sum()
c1 = ((sub1['exposed']==0) & (sub1['event']==1)).sum()
d1 = ((sub1['exposed']==0) & (sub1['event']==0)).sum()
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
