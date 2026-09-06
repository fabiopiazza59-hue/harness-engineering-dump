import pandas as pd, numpy as np
from scipy.stats import chi2

df = pd.read_csv('data.csv')
# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')
# 2. replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# 3. age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['diet_norm'].isin(['mediterranean','usual'])]
# drop missing event
df = df.dropna(subset=['event'])

df['exposed'] = (df['diet_norm']=='mediterranean').astype(int)

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude OR
a = ((df['exposed']==1)&(df['event']==1)).sum()
b = ((df['exposed']==1)&(df['event']==0)).sum()
c = ((df['exposed']==0)&(df['event']==1)).sum()
d = ((df['exposed']==0)&(df['event']==0)).sum()
or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df['site'].dropna().unique())
num_sum = 0.0
den_sum = 0.0
# for variance (RBG)
P_sum = 0.0
Q_sum = 0.0
R_sum = 0.0
S_sum = 0.0

# for MH chi2
sum_a = 0.0
sum_Ea = 0.0
sum_Va = 0.0

site_or = {}
for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['exposed']==1)&(sub['event']==1)).sum()
    bi = ((sub['exposed']==1)&(sub['event']==0)).sum()
    ci = ((sub['exposed']==0)&(sub['event']==1)).sum()
    di = ((sub['exposed']==0)&(sub['event']==0)).sum()
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num_sum += (ai*di)/ni
    den_sum += (bi*ci)/ni
    if bi*ci !=0 and ai*di !=0:
        pass
    # RBG variance components
    Ri = ai*di/ni
    Si = bi*ci/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    P_sum += Ri*Pi
    Q_sum += Ri*Qi + Si*Pi
    R_sum += Si*Qi
    # for chi2
    n1i = ai+bi  # exposed total
    n0i = ci+di  # unexposed total
    m1i = ai+ci  # event total
    m0i = bi+di
    Ei = n1i*m1i/ni
    Vi = (n1i*n0i*m1i*m0i)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ei
    sum_Va += Vi
    if s==1:
        site_or[s] = (ai*di)/(bi*ci) if bi*ci!=0 else np.nan

or_mh = num_sum/den_sum

# RBG variance of ln(OR_MH)
sum_R = num_sum
sum_S = den_sum
var_ln_or = (P_sum/(2*sum_R**2)) + (Q_sum/(2*sum_R*sum_S)) + (R_sum/(2*sum_S**2))
se_ln_or = np.sqrt(var_ln_or)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln_or)
ci_high = np.exp(ln_or + 1.96*se_ln_or)

# MH chi2 with continuity correction
num = (abs(sum_a - sum_Ea) - 0.5)**2
mh_chi2 = num/sum_Va
mh_p = 1 - chi2.cdf(mh_chi2, df=1)

or_site1 = site_or.get(1, np.nan)

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
