
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')

# 1. remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN across all columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

# 5. keep only usual/mediterranean
df = df[df['diet_norm'].isin(['usual','mediterranean'])]

# 6. need event and site not missing
df = df.dropna(subset=['event','site'])

df['exposed'] = (df['diet_norm']=='mediterranean').astype(int)

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude OR
a = ((df['exposed']==1)&(df['event']==1)).sum()
b = ((df['exposed']==1)&(df['event']==0)).sum()
c = ((df['exposed']==0)&(df['event']==1)).sum()
d = ((df['exposed']==0)&(df['event']==0)).sum()
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num_sum = 0.0
den_sum = 0.0
var_sum = 0.0  # for RBG variance
P_sum = 0.0
Q_sum = 0.0
sum_ad_over_n = 0.0
sum_bc_over_n = 0.0

# for MH chi2 continuity corrected
sum_a = 0.0
sum_Ea = 0.0
sum_Va = 0.0

site_data = {}
for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['exposed']==1)&(sub['event']==1)).sum()
    bi = ((sub['exposed']==1)&(sub['event']==0)).sum()
    ci = ((sub['exposed']==0)&(sub['event']==1)).sum()
    di = ((sub['exposed']==0)&(sub['event']==0)).sum()
    ni = ai+bi+ci+di
    site_data[s] = (ai,bi,ci,di,ni)
    if ni==0:
        continue
    num_sum += ai*di/ni
    den_sum += bi*ci/ni
    # RBG variance components
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = ai*di/ni
    Si = bi*ci/ni
    P_sum += Pi*Ri
    Q_sum += Pi*Si + Qi*Ri
    var_sum += Qi*Si
    # MH chi2
    row1 = ai+bi
    row0 = ci+di
    col1 = ai+ci
    col0 = bi+di
    Ei = row1*col1/ni
    Vi = row1*row0*col1*col0/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ei
    sum_Va += Vi

or_mh = num_sum/den_sum

# RBG variance of ln(OR_mh)
R = num_sum
S = den_sum
var_lnOR = P_sum/(2*R**2) + Q_sum/(2*R*S) + var_sum/(2*S**2)
se_lnOR = np.sqrt(var_lnOR)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_lnOR)
ci_high = np.exp(ln_or + 1.96*se_lnOR)

# MH chi2 continuity corrected
numerator = (abs(sum_a - sum_Ea) - 0.5)**2
mh_chi2 = numerator/sum_Va
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site1 OR
ai,bi,ci,di,ni = site_data[1]
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
