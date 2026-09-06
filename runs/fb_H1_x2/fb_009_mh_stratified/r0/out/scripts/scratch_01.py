import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# dedupe exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# age filter
df = df[df['age'].notna()]
df = df[(df['age']>=18)&(df['age']<=80)]
# normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['diet_norm'].isin(['mediterranean','usual'])]

n_total = len(df)
n_exposed = (df['diet_norm']=='mediterranean').sum()

def odds_ratio(sub):
    a = ((sub['diet_norm']=='mediterranean') & (sub['event']==1)).sum()
    b = ((sub['diet_norm']=='mediterranean') & (sub['event']==0)).sum()
    c = ((sub['diet_norm']=='usual') & (sub['event']==1)).sum()
    d = ((sub['diet_norm']=='usual') & (sub['event']==0)).sum()
    return a,b,c,d

a,b,c,d = odds_ratio(df)
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].dropna().unique())
num=0.0; den=0.0
var_num=0.0
Ri_sum=0.0; Si_sum=0.0; PiRi_sum=0.0; PiSi_QiRi_sum=0.0; QiSi_sum=0.0
# for RBG variance
P_sum=0.0; Q_sum=0.0
sum_ad_n=0.0; sum_bc_n=0.0
sum_PR=0.0; sum_PS_QR=0.0; sum_QS=0.0

for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = odds_ratio(sub)
    ni = ai+bi+ci+di
    if ni==0: continue
    num += (ai*di)/ni
    den += (bi*ci)/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR += Pi*Si + Qi*Ri
    sum_QS += Qi*Si
    if s==1:
        or_site1 = (ai*di)/(bi*ci)

or_mh = num/den

# RBG variance of ln(OR_mh)
var_lnOR = sum_PR/(2*num**2) + sum_PS_QR/(2*num*den) + sum_QS/(2*den**2)
se_lnOR = np.sqrt(var_lnOR)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_lnOR)
ci_high = np.exp(ln_or + 1.96*se_lnOR)

# MH chi-square with continuity correction
sum_a=0.0; sum_Ea=0.0; sum_Va=0.0
for s in sites:
    sub = df[df['site']==s]
    ai,bi,ci,di = odds_ratio(sub)
    ni = ai+bi+ci+di
    if ni==0: continue
    n1 = ai+bi  # exposed total
    n0 = ci+di  # unexposed total
    m1 = ai+ci  # event total
    m0 = bi+di
    Ea = n1*m1/ni
    Va = (n1*n0*m1*m0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ea
    sum_Va += Va

mh_chi2 = (abs(sum_a - sum_Ea) - 0.5)**2 / sum_Va
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
    'or_site1': float(or_site1)
}
import json
print(json.dumps(result))
