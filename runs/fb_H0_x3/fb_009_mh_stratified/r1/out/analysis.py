
import pandas as pd
import numpy as np
from scipy.stats import norm

df = pd.read_csv('data.csv')
print('initial', df.shape)

# remove exact duplicates, keep first
df = df.drop_duplicates(keep='first')
print('after dedup', df.shape)

# replace -999 with NaN across all numeric columns
df = df.replace(-999, np.nan)
df = df.replace(-999.0, np.nan)

# age filter 18-80 inclusive, drop missing age
df = df[df['age'].notna()]
df = df[(df['age']>=18) & (df['age']<=80)]
print('after age filter', df.shape)

# normalize diet
df['diet_norm'] = df['diet'].astype(str).str.strip().str.lower()
print(df['diet_norm'].value_counts())

# keep only mediterranean/usual
df = df[df['diet_norm'].isin(['mediterranean','usual'])]
print('after diet filter', df.shape)

# need event, site not missing
df = df[df['event'].notna() & df['site'].notna()]
print('final', df.shape)

n_total = len(df)
n_exposed = (df['diet_norm']=='mediterranean').sum()
print('n_total', n_total, 'n_exposed', n_exposed)

# crude OR
exposed = df['diet_norm']=='mediterranean'
event = df['event']==1
a = ((exposed) & (event)).sum()
b = ((exposed) & (~event)).sum()
c = ((~exposed) & (event)).sum()
d = ((~exposed) & (~event)).sum()
print('crude table', a,b,c,d)
or_crude = (a*d)/(b*c)

# MH pooled OR across sites
sites = sorted(df['site'].unique())
num = 0.0
den = 0.0
# for variance (Robins-Breslow-Greenland)
sum_PR = 0.0
sum_PS_QR = 0.0
sum_QS = 0.0

chi2_num = 0.0
sum_a = 0.0
sum_E = 0.0
sum_V = 0.0

site1_or = None

for s in sites:
    sub = df[df['site']==s]
    a_s = ((sub['diet_norm']=='mediterranean') & (sub['event']==1)).sum()
    b_s = ((sub['diet_norm']=='mediterranean') & (sub['event']==0)).sum()
    c_s = ((sub['diet_norm']=='usual') & (sub['event']==1)).sum()
    d_s = ((sub['diet_norm']=='usual') & (sub['event']==0)).sum()
    n_s = a_s+b_s+c_s+d_s
    if n_s==0:
        continue
    num += (a_s*d_s)/n_s
    den += (b_s*c_s)/n_s
    # RBG variance components
    P_s = (a_s+d_s)/n_s
    Q_s = (b_s+c_s)/n_s
    R_s = (a_s*d_s)/n_s
    S_s = (b_s*c_s)/n_s
    sum_PR += P_s*R_s
    sum_PS_QR += P_s*S_s + Q_s*R_s
    sum_QS += Q_s*S_s
    # MH chi-square components
    E_s = (a_s+b_s)*(a_s+c_s)/n_s
    V_s = (a_s+b_s)*(c_s+d_s)*(a_s+c_s)*(b_s+d_s)/(n_s**2*(n_s-1)) if n_s>1 else 0
    sum_a += a_s
    sum_E += E_s
    sum_V += V_s
    if s==1:
        if b_s==0 or c_s==0:
            site1_or = np.nan
        else:
            site1_or = (a_s*d_s)/(b_s*c_s)
        print('site1', a_s,b_s,c_s,d_s, site1_or)

or_mh = num/den

# variance of ln(OR_MH) - Robins, Breslow, Greenland
ln_or_mh = np.log(or_mh)
var_ln = (sum_PR/(2*num**2)) + (sum_PS_QR/(2*num*den)) + (sum_QS/(2*den**2))
se_ln = np.sqrt(var_ln)
ci_low = np.exp(ln_or_mh - 1.96*se_ln)
ci_high = np.exp(ln_or_mh + 1.96*se_ln)

# MH chi-square with continuity correction
mh_chi2 = (abs(sum_a - sum_E) - 0.5)**2 / sum_V
from scipy.stats import chi2
mh_p = 1 - chi2.cdf(mh_chi2, df=1)

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
