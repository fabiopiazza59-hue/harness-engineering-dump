import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('data.csv')
# remove exact duplicates
df = df.drop_duplicates(keep='first')
# replace -999 sentinel with NaN
df = df.replace(-999, np.nan)
# age filter
df = df[(df['age']>=18) & (df['age']<=80)]
# normalize program
df['program_norm'] = df['program'].astype(str).str.strip().str.lower()
# keep only tutoring/standard
df = df[df['program_norm'].isin(['tutoring','standard'])]
# drop missing event or site
df = df.dropna(subset=['event','site'])

n_total = len(df)
n_exposed = (df['program_norm']=='tutoring').sum()

def table_counts(sub):
    a = ((sub['program_norm']=='tutoring') & (sub['event']==1)).sum()
    b = ((sub['program_norm']=='tutoring') & (sub['event']==0)).sum()
    c = ((sub['program_norm']=='standard') & (sub['event']==1)).sum()
    d = ((sub['program_norm']=='standard') & (sub['event']==0)).sum()
    return a,b,c,d

a,b,c,d = table_counts(df)
or_crude = (a*d)/(b*c)

sites = sorted(df['site'].unique())
num=0.0; den=0.0
var_num=0.0
P_sum=0.0; Q_sum=0.0
R_sum=0.0; S_sum=0.0
sum_a=0; sum_E=0.0; sum_V=0.0

for s in sites:
    sub = df[df['site']==s]
    a_i,b_i,c_i,d_i = table_counts(sub)
    n_i = a_i+b_i+c_i+d_i
    if n_i==0:
        continue
    num += a_i*d_i/n_i
    den += b_i*c_i/n_i
    # RBG variance components
    P_i = (a_i+d_i)/n_i
    Q_i = (b_i+c_i)/n_i
    R_i = a_i*d_i/n_i
    S_i = b_i*c_i/n_i
    P_sum += P_i*R_i
    Q_sum += (P_i*S_i + Q_i*R_i)
    R_sum += R_i
    S_sum += Q_i*S_i
    # for chi2: hypergeometric
    n1_i = a_i+b_i  # exposed total
    n0_i = c_i+d_i  # unexposed total
    m1_i = a_i+c_i  # event total
    m0_i = b_i+d_i
    E_i = n1_i*m1_i/n_i
    V_i = n1_i*n0_i*m1_i*m0_i/(n_i**2*(n_i-1)) if n_i>1 else 0
    sum_a += a_i
    sum_E += E_i
    sum_V += V_i

or_mh = num/den

# RBG variance of ln(OR_MH)
var_ln_or_mh = (P_sum/(2*R_sum**2)) + (Q_sum/(2*R_sum*S_sum)) + (S_sum/(2*S_sum**2))
se_ln = np.sqrt(var_ln_or_mh)
ci_low = np.exp(np.log(or_mh) - 1.96*se_ln)
ci_high = np.exp(np.log(or_mh) + 1.96*se_ln)

chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_V
p_val = 1 - stats.chi2.cdf(chi2, df=1)

# site1 OR
sub1 = df[df['site']==1]
a1,b1,c1,d1 = table_counts(sub1)
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
import json
print(json.dumps(result))
