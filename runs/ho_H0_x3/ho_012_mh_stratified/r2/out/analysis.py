import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN across all columns
df = df.replace(-999, np.nan)

# age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# normalize program
df['program'] = df['program'].astype(str).str.strip().str.lower()

# keep only standard/tutoring
df = df[df['program'].isin(['standard','tutoring'])]

# drop missing event/site
df = df.dropna(subset=['event','site','program'])

n_total = len(df)
n_exposed = int((df['program']=='tutoring').sum())

df['exposed'] = (df['program']=='tutoring').astype(int)

# crude 2x2: exposed/unexposed by event/noevent
a = int(((df.exposed==1) & (df.event==1)).sum())
b = int(((df.exposed==1) & (df.event==0)).sum())
c = int(((df.exposed==0) & (df.event==1)).sum())
d = int(((df.exposed==0) & (df.event==0)).sum())
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num=0; den=0
var_num=0.0
P_sum=0.0
Q_sum=0.0
R_sum=0.0
S_sum=0.0
chi_num_sum=0.0
Oi_sum=0.0
Ei_sum=0.0
Vi_sum=0.0

stratum_data=[]
for s in sites:
    sub = df[df.site==s]
    ai = int(((sub.exposed==1)&(sub.event==1)).sum())
    bi = int(((sub.exposed==1)&(sub.event==0)).sum())
    ci = int(((sub.exposed==0)&(sub.event==1)).sum())
    di = int(((sub.exposed==0)&(sub.event==0)).sum())
    ni = ai+bi+ci+di
    stratum_data.append((ai,bi,ci,di,ni))

for (ai,bi,ci,di,ni) in stratum_data:
    if ni==0: continue
    num += (ai*di)/ni
    den += (bi*ci)/ni

or_mh = num/den

# Robins-Breslow-Greenland variance for ln(OR_MH)
P_sum=0.0
Q_sum=0.0
R_sum=0.0
S_sum=0.0
for (ai,bi,ci,di,ni) in stratum_data:
    if ni==0: continue
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    P_sum += Pi*Ri
    Q_sum += (Pi*Si + Qi*Ri)
    S_sum += Qi*Si
    R_sum += Ri

sum_R = sum((ai*di)/ni for (ai,bi,ci,di,ni) in stratum_data if ni>0)
sum_S = sum((bi*ci)/ni for (ai,bi,ci,di,ni) in stratum_data if ni>0)

var_ln_or = (P_sum/(2*sum_R**2)) + (Q_sum/(2*sum_R*sum_S)) + (S_sum/(2*sum_S**2))
se_ln_or = np.sqrt(var_ln_or)
ln_or_mh = np.log(or_mh)
ci_low = np.exp(ln_or_mh - 1.96*se_ln_or)
ci_high = np.exp(ln_or_mh + 1.96*se_ln_or)

# MH chi-square with continuity correction
sum_ai = sum(ai for (ai,bi,ci,di,ni) in stratum_data)
sum_Eai = 0.0
sum_Vi = 0.0
for (ai,bi,ci,di,ni) in stratum_data:
    if ni==0: continue
    n1i = ai+bi
    n0i = ci+di
    m1i = ai+ci
    m0i = bi+di
    Ei = n1i*m1i/ni
    Vi = (n1i*n0i*m1i*m0i)/(ni**2*(ni-1)) if ni>1 else 0
    sum_Eai += Ei
    sum_Vi += Vi

numerator = (abs(sum_ai - sum_Eai) - 0.5)**2
mh_chi2 = numerator/sum_Vi
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site 1 OR
sub1 = df[df.site==1]
a1 = int(((sub1.exposed==1)&(sub1.event==1)).sum())
b1 = int(((sub1.exposed==1)&(sub1.event==0)).sum())
c1 = int(((sub1.exposed==0)&(sub1.event==1)).sum())
d1 = int(((sub1.exposed==0)&(sub1.event==0)).sum())
or_site1 = (a1*d1)/(b1*c1)

result = {
    'n_total': n_total,
    'n_exposed': n_exposed,
    'or_crude': or_crude,
    'or_mh': or_mh,
    'or_mh_ci_low': ci_low,
    'or_mh_ci_high': ci_high,
    'mh_chi2': mh_chi2,
    'mh_p': mh_p,
    'or_site1': or_site1
}
print(json.dumps(result))
