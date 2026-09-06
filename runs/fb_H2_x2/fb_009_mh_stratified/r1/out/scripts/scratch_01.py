import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter 18-80 inclusive
df = df[(df['age']>=18) & (df['age']<=80)]

# normalize diet
df['diet'] = df['diet'].astype(str).str.strip().str.lower()

# keep valid diet labels, event, site not missing
df = df[df['diet'].isin(['mediterranean','usual'])]
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = (df['diet']=='mediterranean').sum()

# crude 2x2
def make_table(sub):
    a = ((sub['diet']=='mediterranean') & (sub['event']==1)).sum()
    b = ((sub['diet']=='mediterranean') & (sub['event']==0)).sum()
    c = ((sub['diet']=='usual') & (sub['event']==1)).sum()
    d = ((sub['diet']=='usual') & (sub['event']==0)).sum()
    return a,b,c,d

a,b,c,d = make_table(df)
or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df['site'].dropna().unique())
num = 0.0
den = 0.0
sum_a = 0
sum_E = 0.0
sum_V = 0.0
site1_or = None
for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = make_table(sub)
    ni = ai+bi+ci+di
    if ni==0:
        continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # for chi2
    n1 = ai+bi  # exposed total
    n0 = ci+di  # unexposed total
    m1 = ai+ci  # event total
    m0 = bi+di  # no event total
    Ei = n1*m1/ni
    Vi = (n1*n0*m1*m0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_E += Ei
    sum_V += Vi
    if s==1:
        site1_or = (ai*di)/(bi*ci)

or_mh = num/den

# CI via Robins-Breslow-Greenland (RBG) variance
PR_sum=0; PS_sum=0; QR_sum=0; QS_sum=0; RS_sum=0; SR_sum=0
sum_PR=0; sum_PS_QR=0; sum_QS=0
for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = make_table(sub)
    ni = ai+bi+ci+di
    if ni==0:
        continue
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR += Pi*Si + Qi*Ri
    sum_QS += Qi*Si

R_total = num
S_total = den
var_log_or_mh = sum_PR/(2*R_total**2) + sum_PS_QR/(2*R_total*S_total) + sum_QS/(2*S_total**2)
se_log = np.sqrt(var_log_or_mh)
log_or = np.log(or_mh)
ci_low = np.exp(log_or - 1.96*se_log)
ci_high = np.exp(log_or + 1.96*se_log)

# MH chi-square continuity corrected
mh_chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_V
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

result = {
    'n_total': int(n_total),
    'n_exposed': int(n_exposed),
    'or_crude': float(or_crude),
    'or_mh': float(or_mh),
    'or_mh_ci_low': float(ci_low),
    'or_mh_ci_high': float(ci_high),
    'mh_chi2': float(mh_chi2),
    'mh_p': float(mh_p),
    'or_site1': float(site1_or)
}
import json
print(json.dumps(result))
