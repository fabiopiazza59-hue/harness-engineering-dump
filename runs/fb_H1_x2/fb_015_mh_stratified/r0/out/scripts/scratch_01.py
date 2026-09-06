import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# 1. drop exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

# 5. keep only mediterranean/usual
df = df[df['diet_norm'].isin(['mediterranean','usual'])]

# 6. drop missing event
df = df[df['event'].notna()]

df['exposed'] = df['diet_norm']=='mediterranean'

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude 2x2: exposed/unexposed x event/no event
a = int(((df['exposed']==True) & (df['event']==1)).sum())
b = int(((df['exposed']==True) & (df['event']==0)).sum())
c = int(((df['exposed']==False) & (df['event']==1)).sum())
d = int(((df['exposed']==False) & (df['event']==0)).sum())

or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df['site'].dropna().unique())
num = 0.0
den = 0.0
var_sum = 0.0
# for RBG variance
P_sum = 0.0
Q_sum = 0.0
R_sum = 0.0
S_sum = 0.0

E_sum = 0.0
Var_hyper_sum = 0.0
a_total = 0

site_or = {}

for s in sites:
    sub = df[df['site']==s]
    ai = int(((sub['exposed']==True) & (sub['event']==1)).sum())
    bi = int(((sub['exposed']==True) & (sub['event']==0)).sum())
    ci = int(((sub['exposed']==False) & (sub['event']==1)).sum())
    di = int(((sub['exposed']==False) & (sub['event']==0)).sum())
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
    P_sum += Pi*Ri
    Q_sum += Pi*Si + Qi*Ri
    R_sum += Qi*Si
    # hypergeometric moments for MH chi-square
    n1 = ai+bi  # exposed total
    n0 = ci+di  # unexposed total
    m1 = ai+ci  # event total
    m0 = bi+di
    Ei = n1*m1/ni if ni>0 else 0
    Vi = (n1*n0*m1*m0)/(ni**2*(ni-1)) if ni>1 else 0
    E_sum += Ei
    Var_hyper_sum += Vi
    a_total += ai
    if s==1:
        site_or[1] = (ai*di)/(bi*ci) if bi*ci!=0 else np.nan

or_mh = num/den

R_num = sum([ (df[df['site']==s]['exposed']==True).sum()*0 for s in sites ])  # placeholder not used

# RBG variance of ln(OR_mh)
R = num  # sum(ai*di/ni)
S = den  # sum(bi*ci/ni)
var_ln_or = (P_sum/(2*R**2)) + (Q_sum/(2*R*S)) + (R_sum/(2*S**2))
se_ln_or = np.sqrt(var_ln_or)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln_or)
ci_high = np.exp(ln_or + 1.96*se_ln_or)

# MH chi-square continuity corrected
num_chi = (abs(a_total - E_sum) - 0.5)**2
mh_chi2 = num_chi / Var_hyper_sum
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

or_site1 = site_or.get(1, np.nan)

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
