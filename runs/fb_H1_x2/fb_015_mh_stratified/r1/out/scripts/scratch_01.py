import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN across all numeric columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
# age filter
df = df[df['age'].notna() & (df['age']>=18) & (df['age']<=80)]
# normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
# exposed
df['exposed'] = df['diet_norm']=='mediterranean'
# drop missing event
df = df[df['event'].notna()]

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude 2x2 table: exposed/unexposed by event/no event
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
sum_PR = 0.0
sum_PS = 0.0
sum_QR = 0.0
sum_QS = 0.0
R_sum=0.0
S_sum=0.0
chi2_num_sum = 0.0
obs_sum = 0.0
exp_sum = 0.0
var_hyper_sum = 0.0

site_stats = {}
for s in sites:
    sub = df[df['site']==s]
    ai = int(((sub['exposed']==True)&(sub['event']==1)).sum())
    bi = int(((sub['exposed']==True)&(sub['event']==0)).sum())
    ci = int(((sub['exposed']==False)&(sub['event']==1)).sum())
    di = int(((sub['exposed']==False)&(sub['event']==0)).sum())
    ni = ai+bi+ci+di
    if ni==0:
        continue
    site_stats[s] = (ai,bi,ci,di,ni)
    num += (ai*di)/ni
    den += (bi*ci)/ni
    # variance components (Robins-Breslow-Greenland)
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR = Pi*Si + Qi*Ri
    sum_QS += Qi*Si
    R_sum += Ri
    S_sum += Si
    var_hyper_sum += (ai+di)*(ai+ci)*(bi+di)*(bi+ci)/ (ni**2*(ni-1)) if ni>1 else 0
    # for MH chi-square: expected count of a under null, variance
    exp_ai = (ai+bi)*(ai+ci)/ni
    var_ai = (ai+bi)*(ci+di)*(ai+ci)*(bi+di)/(ni**2*(ni-1)) if ni>1 else 0
    obs_sum += ai
    exp_sum += exp_ai
    var_hyper_sum += 0  # already added above, remove duplicate

# recompute properly with clean loop
num=0.0; den=0.0
sum_PR=0.0; sum_PS_QR_total=0.0; sum_QS=0.0
obs_sum=0.0; exp_sum=0.0; var_sum=0.0
for s,(ai,bi,ci,di,ni) in site_stats.items():
    num += (ai*di)/ni
    den += (bi*ci)/ni
    Ri = (ai*di)/ni
    Si = (bi*ci)/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    sum_PR += Pi*Ri
    sum_PS_QR_total += Pi*Si + Qi*Ri
    sum_QS += Qi*Si
    exp_ai = (ai+bi)*(ai+ci)/ni
    var_ai = (ai+bi)*(ci+di)*(ai+ci)*(bi+di)/(ni**2*(ni-1)) if ni>1 else 0
    obs_sum += ai
    exp_sum += exp_ai
    var_sum += var_ai

or_mh = num/den

# Robins-Breslow-Greenland variance of ln(OR_mh)
var_lnOR = sum_PR/(2*num**2) + sum_PS_QR_total/(2*num*den) + sum_QS/(2*den**2)
se_lnOR = np.sqrt(var_lnOR)
ci_low = np.exp(np.log(or_mh) - 1.96*se_lnOR)
ci_high = np.exp(np.log(or_mh) + 1.96*se_lnOR)

# MH chi-square with continuity correction
mh_chi2 = (abs(obs_sum - exp_sum) - 0.5)**2 / var_sum
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site1 OR
ai,bi,ci,di,ni = site_stats[1]
or_site1 = (ai*di)/(bi*ci)

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
import json
print(json.dumps(result))
