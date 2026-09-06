import pandas as pd, numpy as np
from scipy.stats import chi2

df = pd.read_csv('data.csv')
df = df.drop_duplicates(keep='first')
df = df.replace(-999, np.nan)
df = df[(df['age']>=18)&(df['age']<=80)]
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
df = df[df['diet_norm'].isin(['mediterranean','usual'])]
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = int((df['diet_norm']=='mediterranean').sum())

exposed = df['diet_norm']=='mediterranean'
event = df['event']==1

a = int(((exposed) & (event)).sum())
b = int(((exposed) & (~event)).sum())
c = int(((~exposed) & (event)).sum())
d = int(((~exposed) & (~event)).sum())
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
R_sum=0.0
S_sum=0.0
PR_sum=0.0
PS_sum=0.0
QR_sum=0.0
QS_sum=0.0
sum_a=0.0
sum_Ea=0.0
sum_Va=0.0
or_site1=None

for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['diet_norm']=='mediterranean') & (sub['event']==1)).sum()
    bi = ((sub['diet_norm']=='mediterranean') & (sub['event']==0)).sum()
    ci = ((sub['diet_norm']=='usual') & (sub['event']==1)).sum()
    di = ((sub['diet_norm']=='usual') & (sub['event']==0)).sum()
    ni = ai+bi+ci+di
    if ni==0:
        continue
    Ri = ai*di/ni
    Si = bi*ci/ni
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    R_sum += Ri
    S_sum += Si
    PR_sum += Pi*Ri
    PS_sum += Pi*Si
    QR_sum += Qi*Ri
    QS_sum += Qi*Si
    if s==1:
        or_site1 = (ai*di)/(bi*ci)
    ni1 = ai+bi
    ni0 = ci+di
    m1 = ai+ci
    m0 = bi+di
    Ea = ni1*m1/ni
    Va = (ni1*ni0*m1*m0)/(ni**2*(ni-1)) if ni>1 else 0
    sum_a += ai
    sum_Ea += Ea
    sum_Va += Va

or_mh = R_sum/S_sum

var_ln_or = PR_sum/(2*R_sum**2) + (PS_sum+QR_sum)/(2*R_sum*S_sum) + QS_sum/(2*S_sum**2)
se_ln_or = np.sqrt(var_ln_or)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln_or)
ci_high = np.exp(ln_or + 1.96*se_ln_or)

# MH chi-square with continuity correction
num_chi = (abs(sum_a - sum_Ea) - 0.5)**2
mh_chi2 = num_chi/sum_Va
mh_p = 1 - chi2.cdf(mh_chi2, df=1)

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
