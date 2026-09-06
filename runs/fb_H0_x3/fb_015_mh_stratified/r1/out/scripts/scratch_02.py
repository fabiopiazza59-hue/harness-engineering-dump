import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)
df = df[(df['age']>=18) & (df['age']<=80)]
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df.dropna(subset=['diet_norm','event','site'])
df = df[df['diet_norm'].isin(['mediterranean','usual'])]

n_total = len(df)
exposed = df['diet_norm']=='mediterranean'
n_exposed = exposed.sum()

event = df['event']==1

a = ((exposed) & (event)).sum()
b = ((exposed) & (~event)).sum()
c = ((~exposed) & (event)).sum()
d = ((~exposed) & (~event)).sum()
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num_sum = 0.0
den_sum = 0.0
chi_num_sum = 0.0
var_sum = 0.0
R_sum = 0.0
S_sum = 0.0
PR_sum=0.0
PS_QR_sum=0.0
QS_sum=0.0
site_or = {}
for s in sites:
    sub = df[df['site']==s]
    exp = sub['diet_norm']=='mediterranean'
    ev = sub['event']==1
    ai = ((exp)&(ev)).sum()
    bi = ((exp)&(~ev)).sum()
    ci = ((~exp)&(ev)).sum()
    di = ((~exp)&(~ev)).sum()
    ni = ai+bi+ci+di
    if ni==0: continue
    num_sum += ai*di/ni
    den_sum += bi*ci/ni
    Ei = (ai+bi)*(ai+ci)/ni
    Vi = (ai+bi)*(ci+di)*(ai+ci)*(bi+di)/(ni**2*(ni-1)) if ni>1 else 0
    chi_num_sum += (ai - Ei)
    var_sum += Vi
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = ai*di/ni
    Si = bi*ci/ni
    R_sum += Ri
    S_sum += Si
    PR_sum += Pi*Ri
    PS_QR_sum += Pi*Si + Qi*Ri
    QS_sum += Qi*Si
    if s==1:
        site_or[1] = (ai*di)/(bi*ci) if bi*ci!=0 else np.nan

or_mh = num_sum/den_sum

var_lnor = PR_sum/(2*R_sum**2) + PS_QR_sum/(2*R_sum*S_sum) + QS_sum/(2*S_sum**2)
se_lnor = np.sqrt(var_lnor)
ln_or_mh = np.log(or_mh)
ci_low = np.exp(ln_or_mh - 1.96*se_lnor)
ci_high = np.exp(ln_or_mh + 1.96*se_lnor)

mh_chi2 = (abs(chi_num_sum) - 0.5)**2 / var_sum
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
 'or_site1': float(site_or[1])
}
print(json.dumps(result))
