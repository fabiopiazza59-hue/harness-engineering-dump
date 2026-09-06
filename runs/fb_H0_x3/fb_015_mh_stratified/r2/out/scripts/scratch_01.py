import pandas as pd, numpy as np, json

df = pd.read_csv('data.csv')

# 1. remove exact duplicates
df = df.drop_duplicates(keep='first')

# 2. replace -999 with NaN
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# 3. age filter
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# 4. normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()

# 5. drop missing diet, event, site
df = df.dropna(subset=['diet_norm','event','site'])

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
sites = sorted(df['site'].unique())
R_sum=0; S_sum=0; num=0; den=0
P_R_sum=0; P_S_Q_R_sum=0; Q_S_sum=0
sum_a=0; sum_E=0; sum_V=0
site_tables={}
for s in sites:
    sub = df[df['site']==s]
    a_k = ((sub['exposed']==1)&(sub['event']==1)).sum()
    b_k = ((sub['exposed']==1)&(sub['event']==0)).sum()
    c_k = ((sub['exposed']==0)&(sub['event']==1)).sum()
    d_k = ((sub['exposed']==0)&(sub['event']==0)).sum()
    n_k = a_k+b_k+c_k+d_k
    site_tables[s] = (a_k,b_k,c_k,d_k,n_k)
    if n_k==0:
        continue
    R_k = a_k*d_k/n_k
    S_k = b_k*c_k/n_k
    num += R_k
    den += S_k
    P_k = (a_k+d_k)/n_k
    Q_k = (b_k+c_k)/n_k
    R_sum += R_k
    S_sum += S_k
    P_R_sum += P_k*R_k
    P_S_Q_R_sum += P_k*S_k + Q_k*R_k
    Q_S_sum += Q_k*S_k
    E_k = (a_k+b_k)*(a_k+c_k)/n_k
    V_k = (a_k+b_k)*(c_k+d_k)*(a_k+c_k)*(b_k+d_k)/(n_k**2*(n_k-1)) if n_k>1 else 0
    sum_a += a_k
    sum_E += E_k
    sum_V += V_k

or_mh = num/den

var_ln_or_mh = (P_R_sum/(2*R_sum**2)) + (P_S_Q_R_sum/(2*R_sum*S_sum)) + (Q_S_sum/(2*S_sum**2))
se_ln = np.sqrt(var_ln_or_mh)
ln_or = np.log(or_mh)
ci_low = np.exp(ln_or - 1.96*se_ln)
ci_high = np.exp(ln_or + 1.96*se_ln)

# MH chi-square with continuity correction
chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_V
from scipy.stats import chi2 as chi2dist
p_val = 1 - chi2dist.cdf(chi2, df=1)

# site 1 OR
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
 'mh_p': float(p_val),
 'or_site1': float(or_site1)
}
print(json.dumps(result))
