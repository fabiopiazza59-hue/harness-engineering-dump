import pandas as pd, numpy as np, json
from scipy import stats

df = pd.read_csv('data.csv')

df = df.drop_duplicates(keep='first')

df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

df = df[(df['age'] >= 18) & (df['age'] <= 80)]

df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

df = df[df['diet_norm'].isin(['usual', 'mediterranean'])]

df = df.dropna(subset=['event'])

n_total = len(df)
n_exposed = (df['diet_norm'] == 'mediterranean').sum()

df['exposed'] = (df['diet_norm'] == 'mediterranean').astype(int)

a = ((df['exposed']==1) & (df['event']==1)).sum()
b = ((df['exposed']==1) & (df['event']==0)).sum()
c = ((df['exposed']==0) & (df['event']==1)).sum()
d = ((df['exposed']==0) & (df['event']==0)).sum()

or_crude = (a*d)/(b*c)

sites = sorted(df['site'].dropna().unique())
num_sum = 0.0
den_sum = 0.0
E_sum = 0.0
V_sum = 0.0
site_tables = {}
for s in sites:
    sub = df[df['site']==s]
    ai = ((sub['exposed']==1) & (sub['event']==1)).sum()
    bi = ((sub['exposed']==1) & (sub['event']==0)).sum()
    ci = ((sub['exposed']==0) & (sub['event']==1)).sum()
    di = ((sub['exposed']==0) & (sub['event']==0)).sum()
    ni = ai+bi+ci+di
    if ni == 0:
        continue
    site_tables[s] = (ai,bi,ci,di,ni)
    num_sum += (ai*di)/ni
    den_sum += (bi*ci)/ni
    n1i = ai+bi
    n0i = ci+di
    m1i = ai+ci
    m0i = bi+di
    Ei = n1i*m1i/ni
    Vi = (n1i*n0i*m1i*m0i)/(ni**2*(ni-1)) if ni>1 else 0
    E_sum += Ei
    V_sum += Vi

or_mh = num_sum/den_sum

sum_PR = 0.0
sum_PS_QR = 0.0
sum_QS = 0.0
for s,(ai,bi,ci,di,ni) in site_tables.items():
    Pi = (ai+di)/ni
    Qi = (bi+ci)/ni
    Ri = ai*di/ni
    Si = bi*ci/ni
    sum_PR += Pi*Ri
    sum_PS_QR += Pi*Si + Qi*Ri
    sum_QS += Qi*Si

R = num_sum
S = den_sum
var_ln_or = sum_PR/(2*R**2) + sum_PS_QR/(2*R*S) + sum_QS/(2*S**2)
se_ln_or = np.sqrt(var_ln_or)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln_or)
ci_high = np.exp(ln_or + 1.96*se_ln_or)

A_sum = sum(t[0] for t in site_tables.values())
num = abs(A_sum - E_sum) - 0.5
chi2 = (num**2)/V_sum
p_value = 1 - stats.chi2.cdf(chi2, df=1)

a1,b1,c1,d1,n1 = site_tables[1]
or_site1 = (a1*d1)/(b1*c1)

result = {
    'n_total': int(n_total),
    'n_exposed': int(n_exposed),
    'or_crude': float(or_crude),
    'or_mh': float(or_mh),
    'or_mh_ci_low': float(ci_low),
    'or_mh_ci_high': float(ci_high),
    'mh_chi2': float(chi2),
    'mh_p': float(p_value),
    'or_site1': float(or_site1)
}
print(json.dumps(result))
