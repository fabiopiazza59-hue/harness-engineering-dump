import pandas as pd, numpy as np
from scipy import stats
import json

df = pd.read_csv('data.csv')

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')

# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)

# filter age 18-80 inclusive
df = df[(df['age'] >= 18) & (df['age'] <= 80)]

# normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()

# define exposed/unexposed
df = df[df['program_norm'].isin(['tutoring', 'standard'])]

# drop missing event or site
df = df.dropna(subset=['event', 'site'])

df['exposed'] = df['program_norm'] == 'tutoring'

n_total = len(df)
n_exposed = int(df['exposed'].sum())

# crude 2x2 table: exposed/unexposed x event/no event
a = int(((df['exposed']==True) & (df['event']==1)).sum())
b = int(((df['exposed']==True) & (df['event']==0)).sum())
c = int(((df['exposed']==False) & (df['event']==1)).sum())
d = int(((df['exposed']==False) & (df['event']==0)).sum())

or_crude = (a*d)/(b*c)

# stratify by site
sites = sorted(df['site'].unique())
A=[]; B=[]; C=[]; D=[]; N=[]
for s in sites:
    sub = df[df['site']==s]
    ai = int(((sub['exposed']==True) & (sub['event']==1)).sum())
    bi = int(((sub['exposed']==True) & (sub['event']==0)).sum())
    ci = int(((sub['exposed']==False) & (sub['event']==1)).sum())
    di = int(((sub['exposed']==False) & (sub['event']==0)).sum())
    ni = ai+bi+ci+di
    A.append(ai); B.append(bi); C.append(ci); D.append(di); N.append(ni)

A=np.array(A,dtype=float); B=np.array(B,dtype=float); C=np.array(C,dtype=float); D=np.array(D,dtype=float); N=np.array(N,dtype=float)

# MH OR
num = np.sum(A*D/N)
den = np.sum(B*C/N)
or_mh = num/den

# variance for CI (Robins-Breslow-Day-Greenland)
Pi = (A+D)/N
Qi = (B+C)/N
Ri = A*D/N
Si = B*C/N

sum_R = np.sum(Ri)
sum_S = np.sum(Si)

term1 = np.sum(Pi*Ri)/(2*sum_R**2)
term2 = np.sum(Pi*Si + Qi*Ri)/(2*sum_R*sum_S)
term3 = np.sum(Qi*Si)/(2*sum_S**2)

var_log_or_mh = term1 + term2 + term3
se_log_or_mh = np.sqrt(var_log_or_mh)

log_or_mh = np.log(or_mh)
ci_low = np.exp(log_or_mh - 1.96*se_log_or_mh)
ci_high = np.exp(log_or_mh + 1.96*se_log_or_mh)

# MH chi-square with continuity correction
sum_a = np.sum(A)
sum_E = np.sum((A+B)*(A+C)/N)
sum_Var = np.sum((A+B)*(C+D)*(A+C)*(B+D)/(N**2*(N-1)))

mh_chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_Var
mh_p = 1 - stats.chi2.cdf(mh_chi2, df=1)

# site1 OR
idx1 = sites.index(1)
a1,b1,c1,d1 = A[idx1], B[idx1], C[idx1], D[idx1]
or_site1 = (a1*d1)/(b1*c1)

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
